# -*- coding: utf-8 -*-

########### Python 2.7 #############
import httplib, urllib, base64, json, time

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '9732ea3a595942d7bb5e2758982fe6ad',
}

body = {
  "stopWords": [
    "string"
  ],
  "topicsToExclude": [
    "string"
  ],
  "documents": []
}

trumptxt = """Donald J. Trump: You know and ...
Unknown: She used to be great. She's still very beautiful.
Trump: I moved on her, actually. You know, she was down on Palm Beach. I moved on her, and I failed. I'll admit it.
Unknown: Whoa.
Trump: I did try and fuck her. She was married.
Unknown: That's huge news.
Trump: No, no, Nancy. No, this was [unintelligible] — and I moved on her very heavily. In fact, I took her out furniture shopping.
She wanted to get some furniture. I said, “I'll show you where they have some nice furniture.” I took her out furniture —

I moved on her like a bitch. But I couldn't get there. And she was married. Then all of a sudden I see her, she's now got the big phony tits and everything. She's totally changed her look.

Billy Bush: Sheesh, your girl's hot as shit. In the purple.

Trump: Whoa! Whoa!

Bush: Yes! The Donald has scored. Whoa, my man!

[Crosstalk]

Trump: Look at you, you are a pussy.

[Crosstalk]

Trump: All right, you and I will walk out.

[Silence]

Trump: Maybe it's a different one.

Bush: It better not be the publicist. No, it's, it's her, it's —

Trump: Yeah, that's her. With the gold. I better use some Tic Tacs just in case I start kissing her. You know, I'm automatically attracted to beautiful — I just start kissing them. It's like a magnet. Just kiss. I don't even wait. And when you're a star, they let you do it. You can do anything.

Bush: Whatever you want.

Trump: Grab 'em by the pussy. You can do anything.

Bush: Uh, yeah, those legs, all I can see is the legs.

Trump: Oh, it looks good.

Bush: Come on shorty.

Trump: Ooh, nice legs, huh?

Bush: Oof, get out of the way, honey. Oh, that's good legs. Go ahead.

Trump: It's always good if you don't fall out of the bus. Like Ford, Gerald Ford, remember?

Bush: Down below, pull the handle.

Trump: Hello, how are you? Hi!

Arianne Zucker: Hi, Mr. Trump. How are you? Pleasure to meet you.

Trump: Nice seeing you. Terrific, terrific. You know Billy Bush?

Bush: Hello, nice to see you. How you doing, Arianne?

Zucker: Doing very well, thank you. Are you ready to be a soap star?
Trump: We're ready, let's go. Make me a soap star.

Bush: How about a little hug for the Donald? He just got off the bus.

Zucker: Would you like a little hug, darling?

Trump: O.K., absolutely. Melania said this was O.K.

Bush: How about a little hug for the Bushy? I just got off the bus.

Zucker: Bushy, Bushy.

Bush: Here we go. Excellent. Well, you've got a nice co-star here.

Zucker: Yes, absolutely.

Trump: Good. After you.

[Break in video]

Trump: Come on, Billy, don't be shy.

Bush: Soon as a beautiful woman shows up, he just, he takes off. This always happens.

Trump: Get over here, Billy.

Zucker: I'm sorry, come here.

Bush: Let the little guy in here, come on.

Zucker: Yeah, let the little guy in. How you feel now? Better? I should actually be in the middle.

Bush: It's hard to walk next to a guy like this.

Zucker: Here, wait, hold on.

Bush: Yeah, you get in the middle, there we go.
Trump: Good, that's better.

Zucker: This is much better. This is —

Trump: That's better.

Zucker: [Sighs]

Bush: Now, if you had to choose honestly between one of us. Me or the Donald?

Trump: I don't know, that's tough competition.

Zucker: That's some pressure right there.

Bush: Seriously, if you had — if you had to take one of us as a date.

Zucker: I have to take the Fifth on that one.

Bush: Really?

Zucker: Yup — I'll take both.

Trump: Which way?

Zucker: Make a right. Here we go. [inaudible]

Bush: Here he goes. I'm gonna leave you here.

Trump: O.K.

Bush: Give me my microphone.

Trump: O.K. Oh, you're finished?

Bush: You're my man, yeah.

Trump: Oh, good.

Bush: I'm gonna go do our show.

Zucker: Oh, you wanna reset? O.K.
"""

for i in range(100):
	body["documents"].append({
      "id": i+1,
      "text": trumptxt
    })

body = json.dumps(body)

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.0/topics?", body, headers)
    response = conn.getresponse()
    data = response.getheaders()
    operation_location = data[5][1]
    print(operation_location)
    conn.close()
except Exception as e:
    print e

time.sleep(20)

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("GET", operation_location)
    response = conn.getresponse()
    data = response
    print(data.content)
    conn.close()
except Exception as e:
    print e


