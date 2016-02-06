Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 20:32:19) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
 RESTART: D:\Projects\My Final Master Project\code\A_sentiment-based_Ux_System_for_Recommending_Restaurants_According_to_Contextual_Characteristics\SentimentAnalysis\ManagementUnit.py 
[<server>\n<ip>192.168.1.27</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>, <server>\n<ip>192.168.1.20</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>, <server>\n<ip>192.168.1.17</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>, <server>\n<ip>127.0.0.1</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>, <server>\n<ip>192.168.1.18</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>, <server>\n<ip>192.168.1.12</ip>\n<port>1234</port>\n<maxnumberofmsg>1</maxnumberofmsg>\n</server>]
192.168.1.27 1234 1
192.168.1.20 1234 1
192.168.1.17 1234 1
127.0.0.1 1234 1
192.168.1.18 1234 1
192.168.1.12 1234 1
@@@@@@@@@@@@@@@PrintReceivedMsg Enter method
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s
('sentiments_and_feature_for_rest_db',)
1 Exception in thread Thread-1:
Traceback (most recent call last):
  File "C:\Python27\lib\threading.py", line 801, in __bootstrap_inner
    self.run()
  File "C:\Python27\lib\threading.py", line 754, in run
    self.__target(*self.__args, **self.__kwargs)
  File "D:\Projects\My Final Master Project\code\A_sentiment-based_Ux_System_for_Recommending_Restaurants_According_to_Contextual_Characteristics\SentimentAnalysis\QueueConnector\TCPQueueConnector.py", line 31, in __sendDataFromQueue
    self.sendMessage(message)
  File "D:\Projects\My Final Master Project\code\A_sentiment-based_Ux_System_for_Recommending_Restaurants_According_to_Contextual_Characteristics\SentimentAnalysis\QueueConnector\TCPQueueConnector.py", line 53, in sendMessage
    self.sendString(msg)
  File "C:\Python27\lib\site-packages\twisted\protocols\basic.py", line 797, in sendString
    self.transport.write(
AttributeError: 'NoneType' object has no attribute 'write'
/
 139 item id 11682
2 / 139 item id 11682
3 / 139 item id 11682
4 / 139 item id 11682
5 / 139 item id 11682
totalSendItems: 1 / 5 0:00:02.162000
totalSendItems: 2 / 5 0:00:02.508000
6 / 139 item id 11682
7 / 139 item id 11682
8 / 139 item id 11682
totalSendItems: 3 / 8 0:00:03.537000
9 / 139 item id 11682
10 / 139 item id 11682
11 / 139 item id 11682
12 / 139 item id 11682
totalSendItems: 4 / 12 0:00:04.572000
13 / 139 item id 11682
totalSendItems: 5 / 13 0:00:04.926000
14 / 139 item id 11682
15 / 139 item id 11682
16 / 139 item id 11682
totalSendItems: 6 / 16 0:00:05.596000
17 / 139 item id 11682
totalSendItems: 7 / 17 0:00:05.874000
18 / 139 item id 11682
19 / 139 item id 11682
totalSendItems: 8 / 19 0:00:06.344000
20 / 139 item id 11682
totalSendItems: 9 / 20 0:00:06.645000
21 / 139 item id 11682
22 / 139 item id 11682
totalSendItems: 10 / 22 0:00:07.265000
totalSendItems: 11 / 22 0:00:07.497000
23 / 139 item id 11682
totalSendItems: 12 / 23 0:00:07.734000
24 / 139 item id 11682
25 / 139 item id 11682
26 / 139 item id 11682
27 / 139 item id 11682
28 / 139 item id 11682
totalSendItems: 13 / 28 0:00:09.098000
totalSendItems: 14 / 28 0:00:09.235000
29 / 139 item id 11682
30 / 139 item id 11682
31 / 139 item id 11682
32 / 139 item id 11682
33 / 139 item id 11682
totalSendItems: 15 / 33 0:00:10.570000
34 / 139 item id 11682
totalSendItems: 16 / 34 0:00:10.870000
35 / 139 item id 11682
totalSendItems: 17 / 35 0:00:11.119000
36 / 139 item id 11682
totalSendItems: 18 / 36 0:00:11.373000
37 / 139 item id 11682
38 / 139 item id 11682
totalSendItems: 19 / 38 0:00:12.058000
39 / 139 item id 11682
totalSendItems: 20 / 39 0:00:12.321000
40 / 139 item id 11682
41 / 139 item id 11682
42 / 139 item id 11682
totalSendItems: 21 / 42 0:00:13.091000
43 / 139 item id 11682
44 / 139 item id 11682
45 / 139 item id 11682
totalSendItems: 22 / 45 0:00:14.157000
46 / 139 item id 11682
47 / 139 item id 11682
totalSendItems: 23 / 47 0:00:14.568000
48 / 139 item id 11682
totalSendItems: 24 / 48 0:00:14.838000
49 / 139 item id 11682
totalSendItems: 25 / 49 0:00:15.085000
50 / 139 item id 11682
totalSendItems: 26 / 50 0:00:15.339000
51 / 139 item id 11682
52 / 139 item id 11682
53 / 139 item id 11682
totalSendItems: 27 / 53 0:00:16.240000
totalSendItems: 28 / 53 0:00:16.472000
54 / 139 item id 11682
totalSendItems: 29 / 54 0:00:16.641000
55 / 139 item id 11682
56 / 139 item id 11682
totalSendItems: 30 / 56 0:00:17.041000
57 / 139 item id 11682
totalSendItems: 31 / 57 0:00:17.388000
58 / 139 item id 11682
59 / 139 item id 11682
totalSendItems: 32 / 59 0:00:17.921000
60 / 139 item id 11682
totalSendItems: 33 / 60 0:00:18.106000
61 / 139 item id 11682
62 / 139 item id 11682
totalSendItems: 34 / 62 0:00:18.843000
63 / 139 item id 11682
64 / 139 item id 11682
65 / 139 item id 11682
66 / 139 item id 11682
67 / 139 item id 11682
68 / 139 item id 11682
69 / 139 item id 11682
70 / 139 item id 11682
71 / 139 item id 11682
72 / 139 item id 11682
73 / 139 item id 11682
totalSendItems: 35 / 73 0:00:21.966000
74 / 139 item id 11682
totalSendItems: 36 / 74 0:00:22.220000
75 / 139 item id 11682
76 / 139 item id 11682
totalSendItems: 37 / 76 0:00:22.750000
totalSendItems: 38 / 76 0:00:23
77 / 139 item id 11682
78 / 139 item id 11682
79 / 139 item id 11682
80 / 139 item id 11682
totalSendItems: 39 / 80 0:00:24.206000
81 / 139 item id 11682
82 / 139 item id 11682
totalSendItems: 40 / 82 0:00:24.571000
83 / 139 item id 11682
totalSendItems: 41 / 83 0:00:24.818000
totalSendItems: 42 / 83 0:00:25.056000
84 / 139 item id 11682
totalSendItems: 43 / 84 0:00:25.220000
85 / 139 item id 11682
totalSendItems: 44 / 85 0:00:25.487000
86 / 139 item id 11682
87 / 139 item id 11682
totalSendItems: 45 / 87 0:00:26.019000
88 / 139 item id 11682
totalSendItems: 46 / 88 0:00:26.173000
89 / 139 item id 11682
totalSendItems: 47 / 89 0:00:26.558000
90 / 139 item id 11682
totalSendItems: 48 / 90 0:00:26.704000
91 / 139 item id 11682
totalSendItems: 49 / 91 0:00:26.989000
92 / 139 item id 11682
totalSendItems: 50 / 92 0:00:27.183000
93 / 139 item id 11682
totalSendItems: 51 / 93 0:00:27.537000
94 / 139 item id 11682
totalSendItems: 52 / 94 0:00:27.806000
95 / 139 item id 11682
96 / 139 item id 11682
97 / 139 item id 11682
98 / 139 item id 11682
totalSendItems: 53 / 98 0:00:28.977000
99 / 139 item id 11682
totalSendItems: 54 / 99 0:00:29.214000
100 / 139 item id 11682
totalSendItems: 55 / 100 0:00:29.377000
101 / 139 item id 11682
totalSendItems: 56 / 101 0:00:29.693000
102 / 139 item id 11682
103 / 139 item id 11682
totalSendItems: 57 / 103 0:00:30.479000
104 / 139 item id 11682
totalSendItems: 58 / 104 0:00:30.680000
105 / 139 item id 11682
totalSendItems: 59 / 105 0:00:30.965000
106 / 139 item id 11682
totalSendItems: 60 / 106 0:00:31.112000
107 / 139 item id 11682
108 / 139 item id 11682
totalSendItems: 61 / 108 0:00:31.714000
109 / 139 item id 11682
110 / 139 item id 11682
111 / 139 item id 11682
112 / 139 item id 11682
totalSendItems: 62 / 112 0:00:32.815000
113 / 139 item id 11682
114 / 139 item id 11682
totalSendItems: 63 / 114 0:00:33.401000
115 / 139 item id 11682
116 / 139 item id 11682
117 / 139 item id 11682
totalSendItems: 64 / 117 0:00:34.118000
118 / 139 item id 11682
119 / 139 item id 11682
120 / 139 item id 11682
121 / 139 item id 11682
122 / 139 item id 11682
123 / 139 item id 11682
totalSendItems: 65 / 123 0:00:35.690000
124 / 139 item id 11682
totalSendItems: 66 / 124 0:00:35.953000
125 / 139 item id 11682
totalSendItems: 67 / 125 0:00:36.218000
126
