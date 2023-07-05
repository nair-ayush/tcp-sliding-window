# tcp-sliding-window

## Notes

### Receiver

- infinite while loop until terminating message
- store messages received in hashmap????
- receiver's buffer size is NOT the sliding Window, it is just kept so that program runs smoothly without packet loss



### Sender

- send messages
- will need a delimiter (say '\') and a terminator (say '*') for each segment. 
  - eg: a segment may have 1,2,3,4,5 --> it should be sent as seqnumber:1\2\3\4\5*
- window size is determined by (AIMD) receiver's response and has nothing to do with the buffer size of receiver
- track `goodput`
  - `count of messages / tracked number of packets sents`
