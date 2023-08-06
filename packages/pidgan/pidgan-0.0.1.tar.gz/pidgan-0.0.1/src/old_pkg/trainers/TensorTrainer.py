#from __future__ import annotations

import numpy as np
import tensorflow as tf

from datetime import datetime
from html_reports import Report
from lb_pidsim_train.trainers import BaseTrainer


TF_FLOAT = tf.float32
"""Default data-type for tensors."""


class TensorTrainer (BaseTrainer):   # TODO class description
  """Base class for training models in TensorFlow.
  
  Parameters
  ----------
  name : `str`
    Name of the trained model.

  export_dir : `str`, optional
    Export directory for the trained model.

  export_name : `str`, optional
    Export file name for the trained model.

  report_dir : `str`, optional
    Report directory for the trained model.

  report_name : `str`, optional
    Report file name for the trained model.
  """
  def __init__ ( self ,
                 name ,
                 export_dir  = None ,
                 export_name = None ,
                 report_dir  = None ,
                 report_name = None ,
                 verbose = False ) -> None:   # TODO new variable name for warnings
    super().__init__ ( name = name ,
                       export_dir  = export_dir  ,
                       export_name = export_name ,
                       report_dir  = report_dir  ,
                       report_name = report_name ,
                       verbose = verbose )
    self._model_loaded = False   # switch off a new flag

  def feed_from_root_files ( self , 
                             root_files , 
                             X_vars = None , 
                             Y_vars = None , 
                             w_var  = None , 
                             selections = None , 
                             tree_names = None , 
                             chunk_size = None ,
                             verbose = 0 ) -> None:
    """Feed the training procedure with ROOT files.
    
    Parameters
    ----------
    root_files : `str` or `list` of `str`
      List of ROOT files used for the training procedure.

    X_vars : `str` or `list` of `str`, optional
      Branch names of the input variables within the ROOT trees 
      (`None`, by default).

    Y_vars : `str` or `list` of `str`, optional
      Branch names of the output variables within the ROOT trees 
      (`None`, by default).
    
    w_var : `str` or `list` of `str`, optional
      Branch name of the weight variable, if available, within the 
      ROOT trees (`None`, by default).

    selections : `str` or `list` of `str`, optional
      Boolean expressions to filter the ROOT trees (`None`, by default).

    tree_names : `str` or `list` of `str`, optional
      If more than one ROOT tree is defined for each file, the ones to 
      be loaded have to be defined specifying their names as the keys 
      (`None`, by default).

    chunk_size : `int` or `list` of `int`, optional
      Total number of instance rows loaded to disk as `tf.data.Dataset`
      enabling to handle large amount of data (`None`, by default).

    verbose : {0, 1}, optional
      Verbosity mode. `0` = silent (default), `1` = time for data-chunk 
      loading is printed. 

    See Also
    --------
    lb_pidsim_train.utils.data_from_trees :
      Stratified data shuffling from list of `uproot.TTree`.

    tf.data.Dataset :
      Abstraction over a data pipeline that can pull data from several 
      sources, as well as efficiently apply various data transformations.
    """
    super().feed_from_root_files ( root_files = root_files , 
                                   X_vars = X_vars , 
                                   Y_vars = Y_vars , 
                                   w_var  = w_var  , 
                                   selections = selections , 
                                   tree_names = tree_names , 
                                   chunk_size = chunk_size ,
                                   verbose = verbose )

  def prepare_dataset ( self , 
                        X_preprocessing = None , 
                        Y_preprocessing = None , 
                        X_vars_to_preprocess = None , 
                        Y_vars_to_preprocess = None , 
                        subsample_size = 500000 , 
                        save_transformer = True , 
                        verbose = 0 ) -> None:
    if self._model_loaded:
      raise RuntimeError ("error")   # TODO implement error message

    super().prepare_dataset ( X_preprocessing = X_preprocessing , 
                              Y_preprocessing = Y_preprocessing , 
                              X_vars_to_preprocess = X_vars_to_preprocess , 
                              Y_vars_to_preprocess = Y_vars_to_preprocess , 
                              subsample_size = subsample_size , 
                              save_transformer = save_transformer , 
                              verbose = verbose )

    self._w_X = np.copy (self._w)
    self._w_Y = np.copy (self._w)

  def load_model (self) -> None:
    raise NotImplementedError ("error")   # TODO implement error message

  def train_model ( self ,
                    model ,
                    batch_size = 1 ,
                    num_epochs = 1 ,
                    validation_split = 0.0 ,
                    callbacks = None ,
                    produce_report = True ,
                    verbose = 0 ) -> dict:   # TODO complete docstring
    """...
    
    Parameters
    ----------
    model : 
      ...

    batch_size : `int`, optional
      ... (`1`, by default).

    num_epochs : `int`, optional
      ... (`1`, by default).

    validation_split : `float`, optional
      ... (`0.0`, by default).

    callbacks : function, optional
      ... (`None`, by default).

    verbose : {0, 1, 2}, optional
      Verbosity mode. `0` = silent (default), `1` = training progress bar 
      is shown, `2`= one line per training epoch is shown.

    See Also
    --------
    tf.keras.Model.fit :
      Train the model for a fixed number of epochs (iterations on a dataset).
    """
    if not self._dataset_prepared and not self._model_loaded:
      raise RuntimeError ("error")   # TODO implement error message
    elif self._dataset_prepared and self._model_loaded:
      raise RuntimeError ("error")   # TODO implement error message

    ## Data-type control
    try:
      batch_size = self._params.get ( "batch_size", int(batch_size) )
    except:
      raise TypeError ( f"The batch-size should be an integer," 
                        f" instead {type(batch_size)} passed." )
    
    try:
      num_epochs = self._params.get ( "num_epochs", int(num_epochs) )
    except:
      raise TypeError ( f"The number of epochs should be an integer," 
                        f" instead {type(num_epochs)} passed." )

    try:
      validation_split = self._params.get ( "validation_split", float(validation_split) )
    except:
      raise TypeError ( f"The fraction of train-set used for validation should"
                        f" be a float, instead {type(validation_split)} passed." )

    ## Data-value control
    if batch_size <= 0:
      raise ValueError ("error")   # TODO insert error message

    if num_epochs <= 0:
      raise ValueError ("error")   # TODO insert error message

    if (validation_split < 0.0) or (validation_split > 1.0):
      raise ValueError ("error")   # TODO insert error message

    self._batch_size = batch_size
    self._validation_split = validation_split

    ## Sizes computation
    sample_size = self.X . shape[0]
    trainset_size = int ( (1.0 - validation_split) * sample_size )
    steps_per_epoch = max ( 1, int (trainset_size / batch_size) )

    ## Training dataset
    trainset = ( self.X_scaled [:trainset_size] , 
                 self.Y_scaled [:trainset_size] , 
                 self._w_X     [:trainset_size] ,
                 self._w_Y     [:trainset_size] )
    train_ds = self._create_dataset ( trainset, batch_size = batch_size )

    ## Validation dataset
    if validation_split != 0.0:
      valset = ( self.X_scaled [trainset_size:] , 
                 self.Y_scaled [trainset_size:] , 
                 self._w_X     [trainset_size:] ,
                 self._w_Y     [trainset_size:] )
      val_ds = self._create_dataset ( valset, batch_size = batch_size )
    else:
      val_ds = None

    ## Callbacks settings
    if callbacks:
      callbacks = [callbacks]
    else:
      callbacks = None

    ## Training procedure
    start = datetime.now()
    history = model . fit ( train_ds , 
                            epochs = num_epochs , 
                            steps_per_epoch = steps_per_epoch , 
                            validation_data = val_ds ,
                            callbacks = callbacks ,
                            verbose = verbose )
    self._model_trained = True   # switch on model trained flag
    stop = datetime.now()

    timestamp = str(stop-start) . split (".") [0]   # HH:MM:SS
    timestamp = timestamp . split (":")   # [HH, MM, SS]
    timestamp = f"{timestamp[0]}h {timestamp[1]}min {timestamp[2]}s"
    if (verbose > 0): print (f"[INFO] Model training completed in {timestamp}")

    self._model = model

    ## Report setup
    if produce_report:
      report = Report()
      date , hour = str ( datetime.now() ) . split (" ")
      report.add_markdown (f"Report generated on **{date}** at {hour}")
      report.add_markdown (f"Model training completed in **{timestamp}**")
      self._report_params (report)
      self._report_architecture (report, model)
      self._training_plots (report, history)    
      filename = f"{self._report_dir}/{self._report_name}"
      report . write_report ( filename = f"{filename}.html" )

      if (verbose > 0):
        print (f"[INFO] Training report correctly exported to {filename}")

    self._params.clean()
    return history.history

  @staticmethod
  def _create_dataset ( data, batch_size = 100 ) -> tf.data.Dataset:   # TODO complete docstring
    """...
    
    Parameters
    ----------
    data : `tuple`
      ...

    batch_size : `int`, optional
      ... (`100`, by default).

    Returns
    -------
    dataset : `tf.data.Dataset`
      ...

    See Also
    --------
    tf.data.Dataset :
      Abstraction over a data pipeline that can pull data from several 
      sources, as well as efficiently apply various data transformations.
    """
    gpus_avail = len ( tf.config.list_physical_devices ("GPU") ) > 0

    if gpus_avail:
      with tf.device ("/gpu:0"):
        X   = tf.cast ( tf.convert_to_tensor(data[0]), dtype = TF_FLOAT )
        Y   = tf.cast ( tf.convert_to_tensor(data[1]), dtype = TF_FLOAT )
        w_X = tf.cast ( tf.convert_to_tensor(data[2]), dtype = TF_FLOAT )
        w_Y = tf.cast ( tf.convert_to_tensor(data[3]), dtype = TF_FLOAT )
    else:
      with tf.device ("/cpu:0"):
        X   = tf.cast ( tf.convert_to_tensor(data[0]), dtype = TF_FLOAT )
        Y   = tf.cast ( tf.convert_to_tensor(data[1]), dtype = TF_FLOAT )
        w_X = tf.cast ( tf.convert_to_tensor(data[2]), dtype = TF_FLOAT )
        w_Y = tf.cast ( tf.convert_to_tensor(data[3]), dtype = TF_FLOAT )

    dataset = tf.data.Dataset.from_tensor_slices ( (X, Y, w_X, w_Y) )
    dataset = dataset.batch ( batch_size, drop_remainder = True )
    dataset = dataset.cache()
    dataset = dataset.prefetch ( tf.data.AUTOTUNE )
    return dataset

  def _report_params (self, report) -> None:
    report.add_markdown ("---")
    report.add_markdown ('<h2 align="center">Hyperparameters and other details</h2>')
    params_dict = self._params.get_dict()
    text = ""
    for k in params_dict.keys():
      text += f"**{k}** : {params_dict[k]}  \n"
    report.add_markdown (text)

  def _report_architecture (self, report, model) -> str:
    raise NotImplementedError ("error")   # TODO insert error message

  def _training_plots (self, report, history) -> None:
    raise NotImplementedError ("error")   # TODO insert error message

  @property
  def model (self) -> tf.keras.Model:
    """`tf.keras.Model` after the training procedure."""
    return self._model



if __name__ == "__main__":   # TODO complete __main__
  trainer = TensorTrainer ( "test", export_dir = "./models", report_dir = "./reports" )
  trainer . feed_from_root_files ( "../data/Zmumu.root", ["px1", "py1", "pz1"], "E1" )
  print ( trainer.datachunk.describe() )
