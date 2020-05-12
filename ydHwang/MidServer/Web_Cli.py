#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from websocket import create_connection

def client_handle():
    ws = create_connection('ws://0.0.0.0:80/Cocos')

    if ws.connected:
        ws.send('save|User_ID|Test|{"City": "Galle", "Description": "Best damn city in the world"}')
        result = ws.recv()
        print(f"client received:{result}")
        ws.close()

if __name__ == "__main__":
    client_handle()


# In[7]:




# In[ ]:




