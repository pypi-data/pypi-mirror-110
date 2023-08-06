from pdb import set_trace as T
import numpy as np

from collections import defaultdict
from itertools import chain

class Dynamic:
   def __init__(self, env, ent, static, config):
      self.config = config
      self.static = static

      self.data = {}
      self.environment(env, ent)

   @property
   def flat(self):
      return self.data

   def environment(self, env, ent):
      self.data['tile']   = defaultdict(list)
      self.data['entity'] = defaultdict(list)

      R, C = env.shape
      for r in range(R):
         for c in range(C):
            tile = env[r, c]
            self.data['tile'][tile] = self.tile(tile, r, c)

      entities = list(chain.from_iterable(
            [t.ents.values() for t in env.ravel()]))
      for e in entities:
         self.data['entity'][e] = self.entity(ent, e)
         
   def tile(self, tile, r, c):
      stim = {} 

      stim['index'] = tile.state.index
      stim['nEnts'] = tile.nEnts

      #Need to use offsets, not abs coord
      stim['r'] = r
      stim['c'] = c

      return stim

   #Todo: remove the "center" method
   #Todo: make sure we use "other" as the main stim
   #^^^^ MAKE SURE OF THIS ^^^
   def entity(self, ent, targ):
      stim = {} 

      stim['health']    = targ.health.val
      stim['food']      = targ.food.val
      stim['water']     = targ.water.val
      stim['lifetime']  = targ.timeAlive
      stim['damage']    = targ.damage if targ.damage is not None else 0
      stim['freeze']    = targ.freeze

      #Cant use one hot colors because it causes dimensional
      #conflicts when new pops are added at test time
      sameColor = float(ent.colorInd == targ.colorInd)
      stim['sameColor'] = sameColor

      rSelf, cSelf   = ent.pos
      rTarg, cTarg   = targ.pos
      rDelta, cDelta = rTarg - rSelf, cTarg - cSelf

      stim['r'] = rTarg
      stim['c'] = cTarg

      stim['rDelta'] = rDelta
      stim['cDelta'] = cDelta

      return stim

