from pdb import set_trace as T

import os

from neural_mmo.forge.blade import lib
from neural_mmo.forge.trinity.ascend import Ascend, runtime, waittime, Log
from neural_mmo.forge.trinity.timed import Summary

class Trinity():
   def __init__(self, pantheon, god, sword):
      '''Pantheon-God-Sword (Cluster-Server-Core) infra 

      Trinity is three layer distributed infra design pattern for generic, 
      persistent, and asynchronous computation at the Cluster, Server, and
      Core levels. It is built from three user-provided Ascend subclasses, 
      which specify behavior at each layer. Trinity takes advantage of 
      Ascend's builtin performance logging and does not interfere with pdb 
      breakpoint debugging in local mode.
     
      To use Trinity, implement Pantheon, God, and Sword as Ascend subclasses
      to specify Cluster, Server, and Core level execution. Overriding the 
      step() function allows you to perform arbitrary computation and return 
      arbitrary data to the previous layer. Calling super.step() allows you 
      to send and receive arbitrary data to and from the next layer.

      Args:
         pantheon : A subclassed Pantheon class reference
         god      : A subclassed God class reference
         sword    : A subclassed Sword class reference
 
      Notes:
         Ascend is the base API defining distributed infra layers. Trinity is 
         simply three stacked Ascend layers. Ascend and Trinity are not 
         specific computation models: they are design patterns for creating
         computation models. You can implement anything from MPI 
         broadcast-reduce to OpenAI's Rapid to our  MMO style communications
         using Ascend + Trinity with relatively little code and testing.
      '''
      self.pantheon = pantheon
      self.god      = god
      self.sword    = sword

   def init(self, config, args):
      '''
      Instantiates a Pantheon object to make Trinity runnable. Separated
      from __init__ to make Trinity usable as a stuct to hold Pantheon, 
      God, and Sword subclass references

      Args:
         config : A forge.blade.core.Config object
         args   : Additional command line arguments

      Returns:
         self: A self reference
      '''
      lib.ray.init(config, args.ray)
      self.cluster = self.pantheon(self, config, 1)
      self.config  = config
      return self

   def step(self):
      '''Performs one cluster step which trains for one epoch

      Returns:
         txt: Logging string
      '''
      save, stats, log = self.cluster.step()

      log   = Log.summary([self.cluster.discipleLogs(), 
            *log, self.cluster.logs()])
      log   = str(Summary(log))

      #Write stats to txt file
      path = os.path.join(self.config.MODELDIR, self.config.STAT_FILE)
      txt = '\n'.join([save, stats, log])
      with open(path, 'a') as f:
         f.write(txt + '\n')

      return txt
