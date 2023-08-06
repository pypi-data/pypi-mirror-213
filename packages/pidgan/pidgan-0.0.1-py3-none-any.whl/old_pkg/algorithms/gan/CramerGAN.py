#from __future__ import annotations

import tensorflow as tf
from tensorflow.keras.layers        import Dense
from tensorflow.keras.models        import Sequential
from lb_pidsim_train.algorithms.gan import GAN


class Critic:
  """Critic function."""
  def __init__ (self, h):
    self.h = h

  def __call__ (self, x_1, x_2):
    critic_func = tf.norm (self.h(x_1) - self.h(x_2), axis = 1) - tf.norm (self.h(x_1), axis = 1)
    return critic_func


class CramerGAN (GAN):   # TODO add class description
  """Keras model class to build and train CramerGAN system.
  
  Parameters
  ----------
  X_shape : `int` or array_like
    ...

  Y_shape : `int` or array_like
    ...

  discriminator : `list` of `tf.keras.layers`
    ...

  generator : `list` of `tf.keras.layers`
    ...

  latent_dim : `int`, optional
    ... (`64`, by default).

  critic_dim : `int`, optional
    ... (`64`, by default).

  Attributes
  ----------
  discriminator : `tf.keras.Sequential`
    ...

  generator : `tf.keras.Sequential`
    ...

  latent_dim : `int`
    ...

  critic_dim : `int`
    ...

  Notes
  -----
  ...

  References
  ----------
  ...

  See Also
  --------
  ...

  Methods
  -------
  ...
  """
  def __init__ ( self ,
                 X_shape ,
                 Y_shape ,
                 discriminator ,
                 generator     ,
                 referee = None ,
                 latent_dim = 64 ,
                 critic_dim = 64 ) -> None:
    super().__init__ ( X_shape = X_shape ,
                       Y_shape = Y_shape ,
                       discriminator = discriminator , 
                       generator     = generator     ,
                       referee       = referee       ,
                       latent_dim    = latent_dim    )
    self._loss_name = "Energy distance"

    ## Data-type control
    if not isinstance (critic_dim, int):
      if isinstance (critic_dim, float): critic_dim = int (critic_dim)
      else: raise TypeError ("The critic space dimension should be an integer.")

    ## Data-value control
    if critic_dim <= 0:
      raise ValueError ("The critic space dimension should be greater than 0.")

    self._critic_dim = critic_dim

    ## Discriminator sequential model
    self._discriminator = Sequential ( name = "discriminator" )
    for d_layer in discriminator:
      self._discriminator . add ( d_layer )
    self._discriminator . add ( Dense ( units = critic_dim, activation = "linear" , 
                                        kernel_initializer = "glorot_normal" ) )

  def compile ( self , 
                d_optimizer ,
                g_optimizer ,
                r_optimizer = None ,
                d_updt_per_batch = 1 ,
                g_updt_per_batch = 1 ,
                grad_penalty = 10 ) -> None:   # TODO complete docstring
    """Configure the models for CramerGAN training.
    
    Parameters
    ----------
    d_optimizer : `tf.keras.optimizers.Optimizer`
      ...

    g_optimizer : `tf.keras.optimizers.Optimizer`
      ...

    d_updt_per_batch : `int`, optional
      ... (`1`, by default).

    g_updt_per_batch : `int`, optional
      ... (`1`, by default).

    grad_penalty : `float`, optional
      ... (`0.001`, by default).
    """
    super().compile ( d_optimizer = d_optimizer , 
                      g_optimizer = g_optimizer ,
                      r_optimizer = r_optimizer ,
                      d_updt_per_batch = d_updt_per_batch ,
                      g_updt_per_batch = g_updt_per_batch )
    self._critic = Critic ( lambda x : self._discriminator(x) )

    ## Data-type control
    if not isinstance (grad_penalty, float):
      if isinstance (grad_penalty, int): grad_penalty = float (grad_penalty)
      else: raise TypeError ("The loss gradient penalty should be a float.")

    ## Data-value control
    if grad_penalty <= 0:
      raise ValueError ("The loss gradient penalty should be greater than 0.")

    self._grad_penalty = grad_penalty
  
  def _compute_d_loss (self, gen_sample, ref_sample) -> tf.Tensor:   # TODO complete docstring
    """Return the discriminator loss.
    
    Parameters
    ----------
    gen_sample : `tuple` of `tf.Tensor`
      ...

    ref_sample : `tuple` of `tf.Tensor`
      ...

    Returns
    -------
    d_loss : `tf.Tensor`
      ...
    """
    ## Extract input tensors and weights
    XY_gen, w_gen = gen_sample
    XY_ref, w_ref = ref_sample

    ## Data-batch splitting
    batch_size = tf.cast ( tf.shape(XY_gen)[0] / 2, tf.int32 )

    XY_gen_1, XY_gen_2 = XY_gen[:batch_size], XY_gen[batch_size:batch_size*2]
    w_gen_1, w_gen_2 = w_gen[:batch_size], w_gen[batch_size:batch_size*2]

    XY_ref_1 = XY_ref[:batch_size]
    w_ref_1 = w_ref[:batch_size]

    ## Discriminator loss computation
    d_loss = w_gen_1 * w_gen_2 * self._critic ( XY_gen_1, XY_gen_2 ) - \
             w_ref_1 * w_gen_2 * self._critic ( XY_ref_1, XY_gen_2 )
    d_loss = tf.reduce_mean (d_loss, axis = None)

    ## Gradient penalty
    alpha = tf.random.uniform ( shape  = (tf.shape(XY_ref_1)[0], 1) ,
                                minval = 0.0 ,
                                maxval = 1.0 ,
                                dtype  = XY_ref_1.dtype )
    differences  = XY_gen_1 - XY_ref_1
    interpolates = XY_ref_1 + alpha * differences
    critic_int = self._critic ( interpolates , XY_gen_2 )
    grad = tf.gradients ( critic_int , [interpolates] ) [0]
    slopes  = tf.norm ( grad , axis = 1 )
    gp_term = tf.reduce_mean ( tf.square (slopes - 1.0) , axis = None )   # two-sided penalty
    d_loss += self._grad_penalty * gp_term   # gradient penalty
    return d_loss

  def _compute_g_loss (self, gen_sample, ref_sample) -> tf.Tensor:   # TODO complete docstring
    """Return the generator loss.
    
    Parameters
    ----------
    gen_sample : `tuple` of `tf.Tensor`
      ...

    ref_sample : `tuple` of `tf.Tensor`
      ...

    Returns
    -------
    g_loss : `tf.Tensor`
      ...
    """
    ## Extract input tensors and weights
    XY_gen, w_gen = gen_sample
    XY_ref, w_ref = ref_sample

    ## Data-batch splitting
    batch_size = tf.cast ( tf.shape(XY_gen)[0] / 2, tf.int32 )

    XY_gen_1, XY_gen_2 = XY_gen[:batch_size], XY_gen[batch_size:batch_size*2]
    w_gen_1, w_gen_2 = w_gen[:batch_size], w_gen[batch_size:batch_size*2]

    XY_ref_1 = XY_ref[:batch_size]
    w_ref_1 = w_ref[:batch_size]

    ## Generator loss computation
    g_loss = w_ref_1 * w_gen_2 * self._critic ( XY_ref_1, XY_gen_2 ) - \
             w_gen_1 * w_gen_2 * self._critic ( XY_gen_1, XY_gen_2 )
    return tf.reduce_mean (g_loss, axis = None)

  def _compute_threshold (self, ref_sample) -> tf.Tensor:
    """Return the threshold for loss values.
    
    Parameters
    ----------
    ref_sample : `tuple` of `tf.Tensor`
      ...

    Returns
    -------
    th_loss : `tf.Tensor`
      ...
    """
    _, w_ref = ref_sample
    th_loss = tf.zeros_like (w_ref)
    return tf.reduce_sum (th_loss, axis = None)

  @property
  def discriminator (self) -> tf.keras.Sequential:
    """The discriminator of the CramerGAN system."""
    return self._discriminator

  @property
  def generator (self) -> tf.keras.Sequential:
    """The generator of the CramerGAN system."""
    return self._generator

  @property
  def critic_dim (self) -> int:
    """The dimension of the critic space."""
    return self._critic_dim

  @property
  def grad_penalty (self) -> float:
    """Gradient penalty coefficient."""
    return self._grad_penalty
