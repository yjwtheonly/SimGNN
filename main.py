#!/usr/bin/env python
# coding: utf-8

# In[2]:


from train import Trainer


# In[3]:


def main():
    trainer = Trainer(batch_size = 128, epoch_num = 10, val = 0.2)
    trainer.fit()
    trainer.score()


# In[ ]:


if __name__ == "__main__":
    main()

