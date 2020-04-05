#!/usr/bin/env python
# coding: utf-8

# In[5]:


from websocket import create_connection

def client_handle():
    ws = create_connection('ws://0.0.0.0:80/test')
    while True:
        if ws.connected:
            ws.send('hi,i am ws client')
            result = ws.recv()
            print(f"client received:{result}")
            # ws.close()

if __name__ == "__main__":
    client_handle()


# In[7]:


pip install websocket-client


# In[ ]:




