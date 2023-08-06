import tensorflow as tf


class LearningRateSchedulerWithWarmup(tf.optimizers.schedules.LearningRateSchedule):
    
    """ A custom learning rate scheduler for optimizer according to the
    formula in the paper `Attention Is All You Need`.
    Reference: 
    - https://arxiv.org/abs/1706.03762
    """
    
    def __init__(self, d_model=128, warmup_steps=4000):
        super(LearningRateWithWarmup, self).__init__()
        self.d_model = d_model
        self.d_model = tf.cast(self.d_model, tf.float32)
        self.warmup_steps = warmup_steps
    
    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * (self.warmup_steps ** -1.5)
        learning_rate = tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)
        return learning_rate 
