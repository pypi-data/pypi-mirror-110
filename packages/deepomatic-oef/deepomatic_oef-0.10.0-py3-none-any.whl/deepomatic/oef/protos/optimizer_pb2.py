# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deepomatic/oef/protos/optimizer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from deepomatic.oef.protos import hyperparameter_pb2 as deepomatic_dot_oef_dot_protos_dot_hyperparameter__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='deepomatic/oef/protos/optimizer.proto',
  package='deepomatic.oef.optimizer',
  syntax='proto2',
  serialized_pb=_b('\n%deepomatic/oef/protos/optimizer.proto\x12\x18\x64\x65\x65pomatic.oef.optimizer\x1a*deepomatic/oef/protos/hyperparameter.proto\"\x96\x03\n\tOptimizer\x12H\n\x12rms_prop_optimizer\x18\x01 \x01(\x0b\x32*.deepomatic.oef.optimizer.RMSPropOptimizerH\x00\x12I\n\x12momentum_optimizer\x18\x02 \x01(\x0b\x32+.deepomatic.oef.optimizer.MomentumOptimizerH\x00\x12\x41\n\x0e\x61\x64\x61m_optimizer\x18\x03 \x01(\x0b\x32\'.deepomatic.oef.optimizer.AdamOptimizerH\x00\x12\x35\n\x12use_moving_average\x18\x04 \x01(\x08:\x05\x66\x61lseB\x12\xc2>\x06\n\x04\n\x02\x18\x00\xc2>\x06\n\x04\n\x02\x18\x01\x12:\n\x14moving_average_decay\x18\x05 \x01(\x02:\x06\x30.9999B\x14\xc2>\x07\x12\x05\rfff?\xc2>\x07\x12\x05\x15\x00\x00\x80?B>\n\toptimizer\x12\x31\xc2>.\n,\n\x14\"\x12momentum_optimizer\n\x14\"\x12rms_prop_optimizer\"\x8d\x01\n\x10RMSPropOptimizer\x12;\n\x18momentum_optimizer_value\x18\x02 \x01(\x02:\x03\x30.9B\x14\xc2>\x07\x12\x05\r\x00\x00\x00\x00\xc2>\x07\x12\x05\x15\x00\x00\x80?\x12(\n\x05\x64\x65\x63\x61y\x18\x03 \x01(\x02:\x03\x30.9B\x14\xc2>\x07\x12\x05\r\x00\x00\x00\x00\xc2>\x07\x12\x05\x15\x00\x00\x80?\x12\x12\n\x07\x65psilon\x18\x04 \x01(\x02:\x01\x31\"P\n\x11MomentumOptimizer\x12;\n\x18momentum_optimizer_value\x18\x02 \x01(\x02:\x03\x30.9B\x14\xc2>\x07\x12\x05\r\x00\x00\x00\x00\xc2>\x07\x12\x05\x15\x00\x00\x80?\"\x0f\n\rAdamOptimizer\"\xcf\x03\n\x12LearningRatePolicy\x12P\n\x16\x63onstant_learning_rate\x18\x01 \x01(\x0b\x32..deepomatic.oef.optimizer.ConstantLearningRateH\x00\x12\x61\n\x1f\x65xponential_decay_learning_rate\x18\x02 \x01(\x0b\x32\x36.deepomatic.oef.optimizer.ExponentialDecayLearningRateH\x00\x12U\n\x19manual_step_learning_rate\x18\x03 \x01(\x0b\x32\x30.deepomatic.oef.optimizer.ManualStepLearningRateH\x00\x12W\n\x1a\x63osine_decay_learning_rate\x18\x04 \x01(\x0b\x32\x31.deepomatic.oef.optimizer.CosineDecayLearningRateH\x00\x42T\n\x14learning_rate_policy\x12<\xc2>9\n7\n\x1b\"\x19manual_step_learning_rate\n\x18\"\x16\x63onstant_learning_rate\"\x16\n\x14\x43onstantLearningRate\"\xcf\x01\n\x1c\x45xponentialDecayLearningRate\x12\x1e\n\x0f\x64\x65\x63\x61y_steps_pct\x18\x02 \x01(\x02:\x05\x30.006\x12\x1a\n\x0c\x64\x65\x63\x61y_factor\x18\x03 \x01(\x02:\x04\x30.95\x12\x17\n\tstaircase\x18\x04 \x01(\x08:\x04true\x12\x1f\n\x14\x62urnin_learning_rate\x18\x05 \x01(\x02:\x01\x30\x12\x1b\n\x10\x62urnin_steps_pct\x18\x06 \x01(\x02:\x01\x30\x12\x1c\n\x11min_learning_rate\x18\x07 \x01(\x02:\x01\x30\"\xd5\x01\n\x16ManualStepLearningRate\x12W\n\x08schedule\x18\x02 \x03(\x0b\x32\x45.deepomatic.oef.optimizer.ManualStepLearningRate.LearningRateSchedule\x12\x15\n\x06warmup\x18\x03 \x01(\x08:\x05\x66\x61lse\x1aK\n\x14LearningRateSchedule\x12\x10\n\x08step_pct\x18\x01 \x01(\x02\x12!\n\x14learning_rate_factor\x18\x02 \x01(\x02:\x03\x30.1\"\xa5\x01\n\x17\x43osineDecayLearningRate\x12\x1d\n\x0ftotal_steps_pct\x18\x02 \x01(\x02:\x04\x31.07\x12$\n\x14warmup_learning_rate\x18\x03 \x01(\x02:\x06\x30.0002\x12 \n\x10warmup_steps_pct\x18\x04 \x01(\x02:\x06\x30.0025\x12#\n\x18hold_base_rate_steps_pct\x18\x05 \x01(\x02:\x01\x30')
  ,
  dependencies=[deepomatic_dot_oef_dot_protos_dot_hyperparameter__pb2.DESCRIPTOR,])




_OPTIMIZER = _descriptor.Descriptor(
  name='Optimizer',
  full_name='deepomatic.oef.optimizer.Optimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rms_prop_optimizer', full_name='deepomatic.oef.optimizer.Optimizer.rms_prop_optimizer', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='momentum_optimizer', full_name='deepomatic.oef.optimizer.Optimizer.momentum_optimizer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adam_optimizer', full_name='deepomatic.oef.optimizer.Optimizer.adam_optimizer', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='use_moving_average', full_name='deepomatic.oef.optimizer.Optimizer.use_moving_average', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\006\n\004\n\002\030\000\302>\006\n\004\n\002\030\001'))),
    _descriptor.FieldDescriptor(
      name='moving_average_decay', full_name='deepomatic.oef.optimizer.Optimizer.moving_average_decay', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.9999),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\rfff?\302>\007\022\005\025\000\000\200?'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='optimizer', full_name='deepomatic.oef.optimizer.Optimizer.optimizer',
      index=0, containing_type=None, fields=[], options=_descriptor._ParseOptions(descriptor_pb2.OneofOptions(), _b('\302>.\n,\n\024\"\022momentum_optimizer\n\024\"\022rms_prop_optimizer'))),
  ],
  serialized_start=112,
  serialized_end=518,
)


_RMSPROPOPTIMIZER = _descriptor.Descriptor(
  name='RMSPropOptimizer',
  full_name='deepomatic.oef.optimizer.RMSPropOptimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='momentum_optimizer_value', full_name='deepomatic.oef.optimizer.RMSPropOptimizer.momentum_optimizer_value', index=0,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.9),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))),
    _descriptor.FieldDescriptor(
      name='decay', full_name='deepomatic.oef.optimizer.RMSPropOptimizer.decay', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.9),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))),
    _descriptor.FieldDescriptor(
      name='epsilon', full_name='deepomatic.oef.optimizer.RMSPropOptimizer.epsilon', index=2,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=521,
  serialized_end=662,
)


_MOMENTUMOPTIMIZER = _descriptor.Descriptor(
  name='MomentumOptimizer',
  full_name='deepomatic.oef.optimizer.MomentumOptimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='momentum_optimizer_value', full_name='deepomatic.oef.optimizer.MomentumOptimizer.momentum_optimizer_value', index=0,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.9),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=664,
  serialized_end=744,
)


_ADAMOPTIMIZER = _descriptor.Descriptor(
  name='AdamOptimizer',
  full_name='deepomatic.oef.optimizer.AdamOptimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=746,
  serialized_end=761,
)


_LEARNINGRATEPOLICY = _descriptor.Descriptor(
  name='LearningRatePolicy',
  full_name='deepomatic.oef.optimizer.LearningRatePolicy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='constant_learning_rate', full_name='deepomatic.oef.optimizer.LearningRatePolicy.constant_learning_rate', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exponential_decay_learning_rate', full_name='deepomatic.oef.optimizer.LearningRatePolicy.exponential_decay_learning_rate', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manual_step_learning_rate', full_name='deepomatic.oef.optimizer.LearningRatePolicy.manual_step_learning_rate', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cosine_decay_learning_rate', full_name='deepomatic.oef.optimizer.LearningRatePolicy.cosine_decay_learning_rate', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='learning_rate_policy', full_name='deepomatic.oef.optimizer.LearningRatePolicy.learning_rate_policy',
      index=0, containing_type=None, fields=[], options=_descriptor._ParseOptions(descriptor_pb2.OneofOptions(), _b('\302>9\n7\n\033\"\031manual_step_learning_rate\n\030\"\026constant_learning_rate'))),
  ],
  serialized_start=764,
  serialized_end=1227,
)


_CONSTANTLEARNINGRATE = _descriptor.Descriptor(
  name='ConstantLearningRate',
  full_name='deepomatic.oef.optimizer.ConstantLearningRate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1229,
  serialized_end=1251,
)


_EXPONENTIALDECAYLEARNINGRATE = _descriptor.Descriptor(
  name='ExponentialDecayLearningRate',
  full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='decay_steps_pct', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.decay_steps_pct', index=0,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.006),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decay_factor', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.decay_factor', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.95),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='staircase', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.staircase', index=2,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='burnin_learning_rate', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.burnin_learning_rate', index=3,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='burnin_steps_pct', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.burnin_steps_pct', index=4,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_learning_rate', full_name='deepomatic.oef.optimizer.ExponentialDecayLearningRate.min_learning_rate', index=5,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1254,
  serialized_end=1461,
)


_MANUALSTEPLEARNINGRATE_LEARNINGRATESCHEDULE = _descriptor.Descriptor(
  name='LearningRateSchedule',
  full_name='deepomatic.oef.optimizer.ManualStepLearningRate.LearningRateSchedule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='step_pct', full_name='deepomatic.oef.optimizer.ManualStepLearningRate.LearningRateSchedule.step_pct', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='learning_rate_factor', full_name='deepomatic.oef.optimizer.ManualStepLearningRate.LearningRateSchedule.learning_rate_factor', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1602,
  serialized_end=1677,
)

_MANUALSTEPLEARNINGRATE = _descriptor.Descriptor(
  name='ManualStepLearningRate',
  full_name='deepomatic.oef.optimizer.ManualStepLearningRate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='schedule', full_name='deepomatic.oef.optimizer.ManualStepLearningRate.schedule', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='warmup', full_name='deepomatic.oef.optimizer.ManualStepLearningRate.warmup', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MANUALSTEPLEARNINGRATE_LEARNINGRATESCHEDULE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1464,
  serialized_end=1677,
)


_COSINEDECAYLEARNINGRATE = _descriptor.Descriptor(
  name='CosineDecayLearningRate',
  full_name='deepomatic.oef.optimizer.CosineDecayLearningRate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='total_steps_pct', full_name='deepomatic.oef.optimizer.CosineDecayLearningRate.total_steps_pct', index=0,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1.07),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='warmup_learning_rate', full_name='deepomatic.oef.optimizer.CosineDecayLearningRate.warmup_learning_rate', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.0002),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='warmup_steps_pct', full_name='deepomatic.oef.optimizer.CosineDecayLearningRate.warmup_steps_pct', index=2,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.0025),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hold_base_rate_steps_pct', full_name='deepomatic.oef.optimizer.CosineDecayLearningRate.hold_base_rate_steps_pct', index=3,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1680,
  serialized_end=1845,
)

_OPTIMIZER.fields_by_name['rms_prop_optimizer'].message_type = _RMSPROPOPTIMIZER
_OPTIMIZER.fields_by_name['momentum_optimizer'].message_type = _MOMENTUMOPTIMIZER
_OPTIMIZER.fields_by_name['adam_optimizer'].message_type = _ADAMOPTIMIZER
_OPTIMIZER.oneofs_by_name['optimizer'].fields.append(
  _OPTIMIZER.fields_by_name['rms_prop_optimizer'])
_OPTIMIZER.fields_by_name['rms_prop_optimizer'].containing_oneof = _OPTIMIZER.oneofs_by_name['optimizer']
_OPTIMIZER.oneofs_by_name['optimizer'].fields.append(
  _OPTIMIZER.fields_by_name['momentum_optimizer'])
_OPTIMIZER.fields_by_name['momentum_optimizer'].containing_oneof = _OPTIMIZER.oneofs_by_name['optimizer']
_OPTIMIZER.oneofs_by_name['optimizer'].fields.append(
  _OPTIMIZER.fields_by_name['adam_optimizer'])
_OPTIMIZER.fields_by_name['adam_optimizer'].containing_oneof = _OPTIMIZER.oneofs_by_name['optimizer']
_LEARNINGRATEPOLICY.fields_by_name['constant_learning_rate'].message_type = _CONSTANTLEARNINGRATE
_LEARNINGRATEPOLICY.fields_by_name['exponential_decay_learning_rate'].message_type = _EXPONENTIALDECAYLEARNINGRATE
_LEARNINGRATEPOLICY.fields_by_name['manual_step_learning_rate'].message_type = _MANUALSTEPLEARNINGRATE
_LEARNINGRATEPOLICY.fields_by_name['cosine_decay_learning_rate'].message_type = _COSINEDECAYLEARNINGRATE
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy'].fields.append(
  _LEARNINGRATEPOLICY.fields_by_name['constant_learning_rate'])
_LEARNINGRATEPOLICY.fields_by_name['constant_learning_rate'].containing_oneof = _LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy']
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy'].fields.append(
  _LEARNINGRATEPOLICY.fields_by_name['exponential_decay_learning_rate'])
_LEARNINGRATEPOLICY.fields_by_name['exponential_decay_learning_rate'].containing_oneof = _LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy']
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy'].fields.append(
  _LEARNINGRATEPOLICY.fields_by_name['manual_step_learning_rate'])
_LEARNINGRATEPOLICY.fields_by_name['manual_step_learning_rate'].containing_oneof = _LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy']
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy'].fields.append(
  _LEARNINGRATEPOLICY.fields_by_name['cosine_decay_learning_rate'])
_LEARNINGRATEPOLICY.fields_by_name['cosine_decay_learning_rate'].containing_oneof = _LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy']
_MANUALSTEPLEARNINGRATE_LEARNINGRATESCHEDULE.containing_type = _MANUALSTEPLEARNINGRATE
_MANUALSTEPLEARNINGRATE.fields_by_name['schedule'].message_type = _MANUALSTEPLEARNINGRATE_LEARNINGRATESCHEDULE
DESCRIPTOR.message_types_by_name['Optimizer'] = _OPTIMIZER
DESCRIPTOR.message_types_by_name['RMSPropOptimizer'] = _RMSPROPOPTIMIZER
DESCRIPTOR.message_types_by_name['MomentumOptimizer'] = _MOMENTUMOPTIMIZER
DESCRIPTOR.message_types_by_name['AdamOptimizer'] = _ADAMOPTIMIZER
DESCRIPTOR.message_types_by_name['LearningRatePolicy'] = _LEARNINGRATEPOLICY
DESCRIPTOR.message_types_by_name['ConstantLearningRate'] = _CONSTANTLEARNINGRATE
DESCRIPTOR.message_types_by_name['ExponentialDecayLearningRate'] = _EXPONENTIALDECAYLEARNINGRATE
DESCRIPTOR.message_types_by_name['ManualStepLearningRate'] = _MANUALSTEPLEARNINGRATE
DESCRIPTOR.message_types_by_name['CosineDecayLearningRate'] = _COSINEDECAYLEARNINGRATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Optimizer = _reflection.GeneratedProtocolMessageType('Optimizer', (_message.Message,), dict(
  DESCRIPTOR = _OPTIMIZER,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.Optimizer)
  ))
_sym_db.RegisterMessage(Optimizer)

RMSPropOptimizer = _reflection.GeneratedProtocolMessageType('RMSPropOptimizer', (_message.Message,), dict(
  DESCRIPTOR = _RMSPROPOPTIMIZER,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.RMSPropOptimizer)
  ))
_sym_db.RegisterMessage(RMSPropOptimizer)

MomentumOptimizer = _reflection.GeneratedProtocolMessageType('MomentumOptimizer', (_message.Message,), dict(
  DESCRIPTOR = _MOMENTUMOPTIMIZER,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.MomentumOptimizer)
  ))
_sym_db.RegisterMessage(MomentumOptimizer)

AdamOptimizer = _reflection.GeneratedProtocolMessageType('AdamOptimizer', (_message.Message,), dict(
  DESCRIPTOR = _ADAMOPTIMIZER,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.AdamOptimizer)
  ))
_sym_db.RegisterMessage(AdamOptimizer)

LearningRatePolicy = _reflection.GeneratedProtocolMessageType('LearningRatePolicy', (_message.Message,), dict(
  DESCRIPTOR = _LEARNINGRATEPOLICY,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.LearningRatePolicy)
  ))
_sym_db.RegisterMessage(LearningRatePolicy)

ConstantLearningRate = _reflection.GeneratedProtocolMessageType('ConstantLearningRate', (_message.Message,), dict(
  DESCRIPTOR = _CONSTANTLEARNINGRATE,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.ConstantLearningRate)
  ))
_sym_db.RegisterMessage(ConstantLearningRate)

ExponentialDecayLearningRate = _reflection.GeneratedProtocolMessageType('ExponentialDecayLearningRate', (_message.Message,), dict(
  DESCRIPTOR = _EXPONENTIALDECAYLEARNINGRATE,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.ExponentialDecayLearningRate)
  ))
_sym_db.RegisterMessage(ExponentialDecayLearningRate)

ManualStepLearningRate = _reflection.GeneratedProtocolMessageType('ManualStepLearningRate', (_message.Message,), dict(

  LearningRateSchedule = _reflection.GeneratedProtocolMessageType('LearningRateSchedule', (_message.Message,), dict(
    DESCRIPTOR = _MANUALSTEPLEARNINGRATE_LEARNINGRATESCHEDULE,
    __module__ = 'deepomatic.oef.protos.optimizer_pb2'
    # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.ManualStepLearningRate.LearningRateSchedule)
    ))
  ,
  DESCRIPTOR = _MANUALSTEPLEARNINGRATE,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.ManualStepLearningRate)
  ))
_sym_db.RegisterMessage(ManualStepLearningRate)
_sym_db.RegisterMessage(ManualStepLearningRate.LearningRateSchedule)

CosineDecayLearningRate = _reflection.GeneratedProtocolMessageType('CosineDecayLearningRate', (_message.Message,), dict(
  DESCRIPTOR = _COSINEDECAYLEARNINGRATE,
  __module__ = 'deepomatic.oef.protos.optimizer_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.optimizer.CosineDecayLearningRate)
  ))
_sym_db.RegisterMessage(CosineDecayLearningRate)


_OPTIMIZER.oneofs_by_name['optimizer'].has_options = True
_OPTIMIZER.oneofs_by_name['optimizer']._options = _descriptor._ParseOptions(descriptor_pb2.OneofOptions(), _b('\302>.\n,\n\024\"\022momentum_optimizer\n\024\"\022rms_prop_optimizer'))
_OPTIMIZER.fields_by_name['use_moving_average'].has_options = True
_OPTIMIZER.fields_by_name['use_moving_average']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\006\n\004\n\002\030\000\302>\006\n\004\n\002\030\001'))
_OPTIMIZER.fields_by_name['moving_average_decay'].has_options = True
_OPTIMIZER.fields_by_name['moving_average_decay']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\rfff?\302>\007\022\005\025\000\000\200?'))
_RMSPROPOPTIMIZER.fields_by_name['momentum_optimizer_value'].has_options = True
_RMSPROPOPTIMIZER.fields_by_name['momentum_optimizer_value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))
_RMSPROPOPTIMIZER.fields_by_name['decay'].has_options = True
_RMSPROPOPTIMIZER.fields_by_name['decay']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))
_MOMENTUMOPTIMIZER.fields_by_name['momentum_optimizer_value'].has_options = True
_MOMENTUMOPTIMIZER.fields_by_name['momentum_optimizer_value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\302>\007\022\005\r\000\000\000\000\302>\007\022\005\025\000\000\200?'))
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy'].has_options = True
_LEARNINGRATEPOLICY.oneofs_by_name['learning_rate_policy']._options = _descriptor._ParseOptions(descriptor_pb2.OneofOptions(), _b('\302>9\n7\n\033\"\031manual_step_learning_rate\n\030\"\026constant_learning_rate'))
# @@protoc_insertion_point(module_scope)
