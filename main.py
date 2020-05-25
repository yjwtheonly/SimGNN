#!/usr/bin/env python
# coding: utf-8

# In[2]:


from train import Trainer


# In[3]:


def main():
    trainer = Trainer()
    trainer.prepare_for_train(batch_size = 128, epoch_num = 10, val = 0.2)
    trainer.fit()
    trainer.save_model("model.pkl")
    #trainer.load_model("model.pkl")
    trainer.score()


# In[ ]:


if __name__ == "__main__":
    main()

