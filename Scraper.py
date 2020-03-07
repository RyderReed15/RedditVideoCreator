# -*- coding: utf-8 -*-
import praw
import pandas as pd
import datetime as dt
import os 
import subprocess
import imgkit
import sys
from moviepy.editor import *
import moviepy.video as mpe
from pydub import AudioSegment
from pydub.silence import detect_silence
import random
import re
import io




language = 'en'
path = os.path.dirname(os.path.realpath(__file__))


options = {
    'format': 'png',
    'crop-w': '1260',
    'crop-x': '0',
    'crop-y': '0',
    'encoding': "UTF-8"
    }

config = imgkit.config(wkhtmltoimage='C:\Program Files\wkhtmltopdf\\bin\wkhtmltoimage.exe')

reddit = praw.Reddit(client_id='client_id', \
                     client_secret='client_secret', \
                     user_agent='Video creator', \
                     username='username', \
                     password='password')
                     

def getComments(uri='', uris = [], num=40, outputN=0, no=[], name='0'):
    if uri != '' or uris != []:
        if uri != '':

            submission = reddit.submission(url=uri)
            comments = []
            title = submission.title.replace('[SERIOUS]','')
            title = title.replace('-ass','')
            commentsFinal = '<silence msec="2000"/>' + title + '<silence msec="2000"/>'
            titleHTML = '<body style="background-color:#333"><h1 class="h1" style="font-size:72px;text-align:center;color:#fff">' + title.upper() + '</h1>'
            imgkit.from_string(titleHTML, path + "\\comments\\"+str(outputN)+"\\title.png", css=path + '\\title.css',config=config, options=options)
            submission.comments.replace_more(limit=0)
            count = 0
            for top_level_comment in submission.comments:
                if (len(comments) <num and top_level_comment.author != None):
                    if (count not in no):
                    
                        comment = top_level_comment.body
                        comment = comment.replace('–', '-')
                        comment = comment.replace('*', '')
                        comment = comment.replace('~', '')
                        comment = comment.replace('^', '')
                        comment = censorText(comment)
                        
                        html = '<br><body style="background-color:#333"><div class="entry unvoted"><p class="tagline"><a href="javascript:void(0)" class="expand" onclick="return togglecomment(this)"style="padding-top:17px;padding-left:17px;color:#0099dd;font-size:17px">[-]</a><a href="https://www.reddit.com/user/thebrownkid" class="author may-blank id-t2_68nt0" style="color:#0099dd;font-size:17px">'+top_level_comment.author.name+'</a><span class="userattrs"></span><span class="score unvoted" title="23319" style="font-size:17px">' + str(top_level_comment.score)+ ' points</span> <p style="width:964px;padding:8;padding-right:17px;padding-left:17px;font-size:24px;color:#fff">'+comment + '</p></div></div></form><ul class="flat-list buttons"><li class="first"><a href="https://www.reddit.com/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/f6xqgp6/" data-event-action="permalink" class="bylink" rel="nofollow"style="padding-left:17px;color:#0099dd;font-size:17px">permalink </a></li><li><a href="javascript:void(0)" data-comment="/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/f6xqgp6/" data-media="www.redditmedia.com" data-link="/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/" data-root="true" data-title="Now that PBS has announced they\'ll be televising the impeachment hearings, what will the drinking game rules be?" class="embed-comment" style=";color:#0099dd;font-size:17px">embed </a></li><li class="comment-save-button save-button login-required"><a href="javascript:void(0)"style="color:#0099dd;font-size:17px">save </a></li><li class="report-button login-required"><a href="javascript:void(0)" class="reportbtn access-required" data-event-action="report"style=";color:#0099dd;font-size:17px">report </a></li><li class="give-gold-button"><a href="/gold?goldtype=gift&amp;months=1&amp;thing=t1_f6xqgp6" title="give an award in appreciation of this post." class="give-gold login-required access-required gold-give-gold" data-event-action="gild" data-community-awards-enabled="True" rel="nofollow"style=";color:#0099dd;font-size:17px">give award </a></li><li class="reply-button login-required"><a class="access-required" href="javascript:void(0)" data-event-action="comment" onclick="return reply(this)" style="padding-bottom:17px;color:#0099dd;font-size:17px">reply </a></li></ul><div class="reportform report-t1_f6xqgp6"></div></div>'
                        html = html.replace('\n', '<p style="width:964px;padding:8;padding-right:17px;padding-left:17px;font-size:24px;color:#fff">')
                        imgkit.from_string(html, (path + '\\comments\\'+str(outputN)+'\\comment' + str(len(comments)) + '.png'), config=config, css=path + '\\reddit.css', options=options)
                        comment = comment.replace('\n', ' .\n <silence msec="300"/>.')
                        comments.append(comment)
                count+=1
            print("[PROGRESS] Comments Scraped")
            for comment in comments:
                commentsFinal += comment + ' <silence msec="2000"/>'
            commentsFinal += '<silence msec="8000"/>"'
    
            output = io.open(path + '\\comments.txt', 'w+', encoding="utf-8")

            output.write(commentsFinal)
            
            output.close()
            
            subtitles = io.open(path + '\\subtitles\\'+name+'.txt', 'w+', encoding="utf-8")
            sub = commentsFinal.replace('<silence msec="2000"/>', '\n\n')
            sub = sub.replace('<silence msec="8000"/>"', '\n\n')
            sub = sub.replace('.\n <silence msec="300"/>', '\n')
            subtitles.write(sub)
            print("[PROGRESS] Subtitles Written")
            subtitles.close()
            
            subprocess.run(path + '\\speak\\balcon -s ".95" -w "'  +path + '\\output['+str(outputN+1)+'].wav" -f "'+path + '\\comments.txt"')
            
            
            print('[DONE]')
        elif uris != []:
            count = 0
            for url in uris:
                count+=1
                submission = reddit.submission(url=url)
                comments = []
                commentsFinal = '<silence msec="2000"/>' + submission.title + '<silence msec="7000"/>'
                titleHTML = '<body style="background-color:#333"><h1 class="h1" style="font-size:72px;text-align:center;color:#fff">' + submission.title.upper() + '</h1>'
                imgkit.from_string(titleHTML, path + "\\comments\\"+str(count-1)+"\\title.png", css=path + '\\title.css',config=config, options=options)
                submission.comments.replace_more(limit=0)
                for top_level_comment in submission.comments:
                    if (len(comments) <num and top_level_comment.author != None ):
                        comment = top_level_comment.body
                        comment = comment.replace('–', '-')
                        comment = comment.replace('*', '')
                        comment = comment.replace('~', '')
                        comment = comment.replace('^', '')
                        comment = censorText(comment)
                        
                        html = '<br><body style="background-color:#333"><div class="entry unvoted"><p class="tagline"><a href="javascript:void(0)" class="expand" onclick="return togglecomment(this)"style="padding-top:17px;padding-left:17px;color:#0099dd;font-size:17px">[-]</a><a href="https://www.reddit.com/user/thebrownkid" class="author may-blank id-t2_68nt0" style="color:#0099dd;font-size:17px">'+top_level_comment.author.name+'</a><span class="userattrs"></span><span class="score unvoted" title="23319" style="font-size:17px">' + str(top_level_comment.score)+ ' points</span> <p style="width:964px;padding:8;padding-right:17px;padding-left:17px;font-size:24px;color:#fff">'+comment + '</p></div></div></form><ul class="flat-list buttons"><li class="first"><a href="https://www.reddit.com/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/f6xqgp6/" data-event-action="permalink" class="bylink" rel="nofollow"style="padding-left:17px;color:#0099dd;font-size:17px">permalink </a></li><li><a href="javascript:void(0)" data-comment="/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/f6xqgp6/" data-media="www.redditmedia.com" data-link="/r/AskReddit/comments/dtmyxw/now_that_pbs_has_announced_theyll_be_televising/" data-root="true" data-title="Now that PBS has announced they\'ll be televising the impeachment hearings, what will the drinking game rules be?" class="embed-comment" style=";color:#0099dd;font-size:17px">embed </a></li><li class="comment-save-button save-button login-required"><a href="javascript:void(0)"style="color:#0099dd;font-size:17px">save </a></li><li class="report-button login-required"><a href="javascript:void(0)" class="reportbtn access-required" data-event-action="report"style=";color:#0099dd;font-size:17px">report </a></li><li class="give-gold-button"><a href="/gold?goldtype=gift&amp;months=1&amp;thing=t1_f6xqgp6" title="give an award in appreciation of this post." class="give-gold login-required access-required gold-give-gold" data-event-action="gild" data-community-awards-enabled="True" rel="nofollow"style=";color:#0099dd;font-size:17px">give award </a></li><li class="reply-button login-required"><a class="access-required" href="javascript:void(0)" data-event-action="comment" onclick="return reply(this)" style="padding-bottom:17px;color:#0099dd;font-size:17px">reply </a></li></ul><div class="reportform report-t1_f6xqgp6"></div></div>'
                        html = html.replace('\n', '<p style="width:964px;padding:8;padding-right:17px;padding-left:17px;font-size:24px;color:#fff">')
                        imgkit.from_string(html, (path + '\\comments\\'+str(count-1)+'\comment' + str(len(comments)) + '.png'), config=config, css=path + '\\reddit.css', options=options)
                        comment = comment.replace('\n', ' .\n <silence msec="300"/>.')
                        comments.append(comment)
                print("[PROGRESS] Comments Scraped")
                for comment in comments:
                    commentsFinal += comment + ' \n . <silence msec="2000"/>'
                commentsFinal += '<silence msec="8000"/>'
        
                output = open(path + '\\comments.txt', 'w+')
                output.write(commentsFinal)
                output.close()
                
                subprocess.run(path + '\\speak\\balcon -s ".95" -w "'+ path + '\\output[ ' + str(count) + '].wav" -f "'+path + '\\comments.txt"')
                print("[PROGRESS] Text Converted")
                
                print('[DONE]')

        
   
def makeVideo(num=1,out="out.mp4"):
    audio=path + "\\output["+str(num)+"].wav"
    commentPath=path + "\\comments\\"+str(num-1)+"\\"
    seg = AudioSegment.from_wav(audio)
    base = random.randint(1,2)
    audioShots=[]
    silences = detect_silence(seg,1800,-32)
    shots = []
    speech = AudioFileClip(audio)

    video = (VideoFileClip(path + "\\video\Base"+str(base)+".mp4")
            .set_end(seg.duration_seconds))
    audioClip = video.audio
    shots.append(video)
    clip = ( ImageClip(commentPath+"title.png")
             .set_position('center')
             .set_start((silences[0][1]/1000)-0.5)
             .set_end((silences[1][0]/1000)+0.25) )
    
    shots.append(clip)




    for i in range(1,len(silences)-1):
        if i != len(silences)-1:
            image = ( ImageClip(commentPath+"comment"+str(i-1)+".png")
                    .set_position('center')
                    .set_start((silences[i][1]/1000)-0.4)
                    .set_end((silences[i+1][1]/1000)-0.75) )
            

            
        else:
            image = ( ImageClip(commentPath+"comment"+str(i-1)+".png")
                    .set_position('center')
                    .set_start((silences[i][1]/1000)-0.4)
                    .set_end(seg.duration_seconds-9.75) )
                    
        static = ( VideoFileClip(path + "\\video\static.mp4")
                    .set_position('center')
                    .set_start((silences[i][1]/1000)-0.75)
                    .set_end((silences[i][1]/1000)-0.4) )
        stat_audio = static.audio
        wScale = (1920/image.w)
        hScale = (1080/image.h)
        if wScale >= hScale:
            image = image.resize(newsize=hScale)
        else:
            image = image.resize(newsize=wScale)
            
        shots.append(image)
        shots.append(static)
        static.close()
        image.close()
        audioShots.append(stat_audio)
        stat_audio.close()
    audioShots.append(audioClip)
    audioShots.append(speech)
    result = CompositeVideoClip(shots) # Overlay text on video
    compAudio = CompositeAudioClip(audioShots)
    result = result.set_audio(compAudio)


    result.write_videofile(path + "\\video\\"+out,fps=25)
    video.close()
    clip.close()
    audioClip.close()
    for s in shots:
        s.close()
    for a in audioShots:
        a.close()
    
    
def makeVideos(start=0, count=1):
    if count < start or start == None or count == None:
        print('Please enter a starting number, and an end number. End must be greater than start')
        return
    else:
        for i in range(start,count):
            makeVideo(num=(i+1),out ="out["+str(i)+"].mp4")
    

def censorText(text):
    # could be done using a file with the word and the censored version but whatever
    exp1 = re.compile(re.escape(' fuck'), re.IGNORECASE)
    exp20 = re.compile(re.escape('dumbfuck'), re.IGNORECASE)
    exp2 = re.compile(re.escape(' ass '), re.IGNORECASE)
    exp19 = re.compile(re.escape('asshole'), re.IGNORECASE)
    exp21 = re.compile(re.escape('shitt'), re.IGNORECASE)
    exp3 = re.compile(re.escape('shit'), re.IGNORECASE)
    exp4 = re.compile(re.escape(' cunt'), re.IGNORECASE)
    exp5 = re.compile(re.escape(' dick'), re.IGNORECASE)
    exp6 = re.compile(re.escape(' cock'), re.IGNORECASE)
    exp7 = re.compile(re.escape(' bitch'), re.IGNORECASE)
    exp8 = re.compile(re.escape('faggot'), re.IGNORECASE)
    exp9 = re.compile(re.escape('fag'), re.IGNORECASE)
    exp10 = re.compile(re.escape('bastard'), re.IGNORECASE)
    exp11 = re.compile(re.escape('whore'), re.IGNORECASE)
    exp12 = re.compile(re.escape(' prick'), re.IGNORECASE)
    exp13 = re.compile(re.escape('nigger'), re.IGNORECASE)
    exp14 = re.compile(re.escape('nigga'), re.IGNORECASE)
    exp15 = re.compile(re.escape('damn'), re.IGNORECASE)
    exp16 = re.compile(re.escape('hitler'), re.IGNORECASE)
    exp22 = re.compile(re.escape('sex'), re.IGNORECASE)
    exp17 = re.compile('\\[.*\\]\\(.*\\)', re.IGNORECASE)
    exp18 = re.compile('\\[.*\\]', re.IGNORECASE)
    res = exp17.findall(text)
    if res != [] or res !=None:
        for x in res:
            g = x.split(',  ')
            for i in g:
                temp = exp17.sub(exp18.search(i).group(), i, count=1)
                exp = re.compile(re.escape(i), re.IGNORECASE)
                temp = temp.replace('[', '')
                temp = temp.replace(']','')
                text = exp.sub(temp, text)
    text = exp1.sub(' frick', text)
    text = exp20.sub('dumbfrick', text)
    text = exp2.sub(' butt', text)
    text = exp19.sub('butthole', text)
    text = exp21.sub('crapp', text)
    text = exp3.sub('crap', text)
    text = exp4.sub(' c*nt', text)
    text = exp5.sub(' d*ck', text)
    text = exp6.sub(' c*ck', text)
    text = exp7.sub(' b*tch', text)
    text = exp8.sub('homosexual', text)
    text = exp9.sub('gay', text)
    text = exp10.sub('b****rd', text)
    text = exp11.sub('w****', text)
    text = exp12.sub(' pr**k', text)
    text = exp13.sub('n-word', text)
    text = exp14.sub('n-word', text)
    text = exp15.sub('dang', text)
    text = exp16.sub('H*tler', text)
    text = exp22.sub('s*x', text)
    return text
  

    
    