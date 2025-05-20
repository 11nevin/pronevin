from django.shortcuts import render, redirect
from summary.models import *
import moviepy as mp
import speech_recognition as sr
from transformers import pipeline
import cv2
from pathlib import Path
from moviepy import VideoFileClip
from django.core.files.storage import FileSystemStorage
import requests as rs
import os
import speech_recognition as sr 
import os 
from django.db.models import Count, Q
from pydub import AudioSegment
from pydub.silence import split_on_silence
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from lexrank import LexRank
from lexrank import STOPWORDS
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from transformers import pipeline
from datetime import datetime, timezone
import time
import re
import random
from django.db.models import Q
from gtts import gTTS
import os
from django.conf import settings
from googletrans import Translator 

# NEW IMPORTS FOR VOICE COMMAND FEATURE
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

action_words = [
    'abandon', 'accelerate', 'accept', 'access', 'accomplish', 'accuse', 'achieve', 'acknowledge', 'acquire', 'adapt',
    'add', 'adhere', 'adjust', 'administer', 'admit', 'adopt', 'advance', 'advertise', 'advice', 'affect',
    'affirm', 'afford', 'agree', 'aim', 'allege', 'amplify', 'analyze', 'announce', 'annoy', 'answer',
    'anticipate', 'appeal', 'apply', 'argue', 'arrange', 'arrive', 'ask', 'assert', 'assault', 'assess',
    'assign', 'assume', 'attempt', 'attend', 'attract', 'avoid', 'balance', 'ban', 'be', 'believe', 'blame',
    'boost', 'borrow', 'bounce', 'break', 'bring', 'build', 'calculate', 'call', 'cancel', 'capture', 'care',
    'cause', 'change', 'check', 'clarify', 'clean', 'close', 'coach', 'collect', 'combine', 'come', 'compare',
    'compete', 'complete', 'comply', 'conduct', 'confirm', 'connect', 'contribute', 'convince', 'create', 'criticize',
    'decide', 'define', 'delegate', 'deliver', 'demand', 'deny', 'depend', 'describe', 'destroy', 'determine',
    'develop', 'direct', 'disagree', 'discover', 'dismiss', 'distinguish', 'distribute', 'divide', 'do', 'dominate',
    'doubt', 'download', 'draw', 'educate', 'elect', 'eliminate', 'embark', 'encourage', 'endorse', 'enforce',
    'enjoy', 'ensure', 'enter', 'establish', 'evaluate', 'examine', 'exclude', 'expand', 'expect', 'explain',
    'explore', 'expose', 'extend', 'facilitate', 'fear', 'feel', 'finish', 'fix', 'focus', 'follow', 'force',
    'forget', 'form', 'foster', 'gather', 'generate', 'get', 'give', 'go', 'grow', 'handle', 'have', 'help',
    'highlight', 'hire', 'hold', 'hope', 'identify', 'ignore', 'illustrate', 'imagine', 'impact', 'implement',
    'impress', 'improve', 'include', 'increase', 'initiate', 'instruct', 'integrate', 'interact', 'interrupt', 'introduce',
    'invest', 'invite', 'involve', 'judge', 'justify', 'keep', 'know', 'launch', 'learn', 'let', 'like', 'listen',
    'locate', 'maintain', 'manage', 'mark', 'measure', 'motivate', 'navigate', 'need', 'notice', 'observe', 'offer',
    'open', 'opt', 'organize', 'overcome', 'participate', 'perform', 'plan', 'play', 'prepare', 'present', 'press',
    'proceed', 'produce', 'promote', 'propose', 'protect', 'prove', 'provide', 'publish', 'pursue', 'question',
    'quote', 'read', 'realize', 'receive', 'reduce', 'refer', 'reject', 'relate', 'release', 'rely', 'remark',
    'remove', 'repeat', 'replace', 'report', 'represent', 'request', 'respond', 'review', 'revise', 'risk',
    'rule', 'run', 'satisfy', 'save', 'search', 'select', 'send', 'set', 'share', 'show', 'simplify', 'skip',
    'solve', 'speak', 'stand', 'start', 'stimulate', 'strengthen', 'study', 'submit', 'succeed', 'suggest',
    'support', 'survive', 'sustain', 'take', 'talk', 'teach', 'terminate', 'test', 'thank', 'think', 'train',
    'translate', 'treat', 'try', 'turn', 'understand', 'use', 'verify', 'view', 'visit', 'vote', 'warn',
    'watch', 'win', 'work', 'write', 'yield', 'zoom'
]

# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media') 

def index(request):
    return render(request, "index.html")

def userregistration(request):
    msg = ""
    if request.POST:
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['password']
        qualif = request.POST['qualif']
        address = request.POST['address']
        purpose = request.POST['purpose']

        email_check = Login.objects.filter(username=email).exists()
        contact_check = User.objects.filter(contact=contact).exists()
        if email_check:
            msg = 'Email Already Registered'
        elif contact_check:
            msg = 'Contact Number Already Used'
        else:
            try:
                # login_user = Login.objects.create_user(username=email, email=email, password=password, user_type='User', question=question, answer=answer)
                login_user = Login.objects.create_user(username=email, email=email, password=password, user_type='User')
                register_user = User.objects.create(firstname=fname, lastname=lname, age=age, contact=contact, qualification=qualif, purpose=purpose, address=address, email=email, loginid=login_user)
                register_user.save()
                login_user.save()
                msg = 'User Registered Successfully'
            except:
                msg = 'Error Occurred While Registering'
    return render(request, "userregistration.html", {'msg': msg})

def login(request):
    msg = ""
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            email_check = Login.objects.get(username=email)
            password_check = email_check.check_password(password)
            if not email_check.is_active:
                msg = "Account Deleted"
            elif password_check == False:
                msg = "Password Entered is Wrong"
            else:
                request.session['uid'] = email_check.id
                if email_check.user_type == "User":
                    return redirect(f'/userhome?user={email_check.id}')
                elif email_check.is_superuser == True:
                    return redirect(f'/adminhome?user={email_check.id}')
                else:
                    msg = "Invalid Usertype"
        except:
            msg = "Email Not Registered"    
    return render(request, 'login.html', {'msg': msg})

def videosummary(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    msg = ""
    summary = ""

    if request.POST:
        video = request.FILES['video']  # Keep the variable name as 'video' for consistency
        fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'static', 'media'))
        filename = fs.save(video.name, video)
        file_path = fs.path(filename)  # Full path to the saved file
        print(file_path, "----------------------------------")
        # Check file type (audio or video)
        file_extension = os.path.splitext(file_path)[1].lower()
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac']
        if file_extension not in audio_extensions:
            msg = "Please upload a valid audio file."
            return render(request, "videosummary.html", {'msg': msg, 'summary': summary})

        # Process the audio file directly
        transcription = process_audio_chunks(file_path)
        summaries = text_summary(transcription)
        summary = summaries["abstractive"]

        # Save to video history (variable names unchanged)
        history = Video_History.objects.create(user=user, video=f"/static/media/{video.name}", summary=summary)
        history.save()
    return render(request, "videosummary.html", {'msg': msg, 'summary': summary})

def text_summary(text):
    nltk.download('stopwords')
    nltk.download('punkt_tab')
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    word_freq = Counter(filtered_words)
    top_words = [word for word, _ in word_freq.most_common(5)]

    sentences = sent_tokenize(text)
    summary_sentences = [sentence for sentence in sentences if any(word in sentence.lower() for word in top_words)]
    extractive_summary = " ".join(summary_sentences)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    abstractive_summary = summarizer(extractive_summary, max_length=100, min_length=30, do_sample=False)

    return {
        "extractive": extractive_summary,
        "abstractive": abstractive_summary[0]["summary_text"]
    }

def adminhome(request):
    try:
        msg = "Welcome Admin"
    except:
        pass
    return render(request, "adminindex.html", {'msg': msg})

def transcribe_audio(path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Unable to transcribe audio."

# Audio Chunk Processing
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def process_audio_chunks(audio_path):
    try:
        sound = AudioSegment.from_file(audio_path)  # Ensure correct file format
        chunks = split_on_silence(
            sound, 
            min_silence_len=500, 
            silence_thresh=sound.dBFS - 14, 
            keep_silence=500
        )
    except FileNotFoundError:
        print(f"File not found: {audio_path}")
        return "Error: File not found."
    except CouldntDecodeError:
        print(f"Error decoding file: {audio_path}")
        return "Error: Could not decode audio file."

    transcription = ""
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(BASE_DIR, f"static/media/audio_chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")
        transcription += transcribe_audio(chunk_path) + " "
        os.remove(chunk_path)  # Clean up temporary chunk files
    return transcription

def userhome(request):
    return render(request, "userindex.html")

def user_video_history(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    data_video = Video_History.objects.filter(user=user)
    data_text = Text_History.objects.filter(user=user)
    count = data_video.count()
    return render(request, "uservideohistory.html", {'data': data_video, 'data2': data_text, 'count': count})

def user_profile(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    msg = ""
    if request.POST:
        try:
            fname = request.POST['fname']
            lname = request.POST['lname']
            age = request.POST['age']
            contact = request.POST['contact']
            qualif = request.POST['qualif']
            address = request.POST['address']
            purpose = request.POST['purpose']
            user.firstname = fname
            user.lastname = lname
            user.age = age
            user.contact = contact
            user.qualification = qualif
            user.address = address
            user.purpose = purpose
            user.save()
            msg = "Updated Successfully"
        except:
            msg = "Qualification and Purpose Must be selected again make sure you selected it "
    return render(request, "userprofile.html", {'data': user, 'msg': msg})

def deleteuserprofile(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = 0
    user.save()
    return redirect('/login')

def admin_user(request):
    data = User.objects.all()
    return render(request, "adminusers.html", {'data': data})

def admin_user_details(request):
    uid = request.GET['uid']
    user = User.objects.get(loginid__id=uid)
    return render(request, "adminuserdetails.html", {'data': user})

def admin_user_active(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = True
    user.save()
    return redirect(f'/admin_user_details?uid={uid}')

def admin_user_inactive(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = False
    user.save()
    return redirect(f'/admin_user_details?uid={uid}')

def user_feedback(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=request.session.get('uid'))
    msg = ""
    feeds = Feedback.objects.filter(user=user)
    if request.POST:
        try:
            rating = request.POST['star_rating']
            feed = request.POST['inputtext']
            feedback = Feedback.objects.create(user=user, feedback=feed, rating=rating)
            feedback.save()
            msg = "Feedback Added"
        except:
            msg = "Click Any Star"
    return render(request, "userfeedback.html", {'msg': msg, 'feeds': feeds})

def admin_feedbacks(request):
    data = Feedback.objects.all()
    msg = ''
    if request.POST:
        fid = request.POST['fid']
        feed = request.POST['reply']
        feedback = Feedback.objects.get(id=fid)
        feedback.reply = feed
        feedback.save()
        msg = "Reply Added Successfully"
    return render(request, "adminfeedbacks.html", {'data': data, 'msg': msg})

def user_premium(request):
    data = Premium.objects.all()
    today = datetime.now(timezone.utc)
    print(today, '*********************')
    for d in data:
        if ( today > d.offer_till ):
            d.delete()
    return render(request, "userpremium.html", {'data': data})

def admin_premium(request):
    packages = Premium.objects.all()
    count = packages.count()
    msg = ''
    if request.POST:
        months = request.POST['months']
        realprice = request.POST['realprice']
        offertill = request.POST['offertill'] 
        offertil = request.POST['offertil']
        offerprice = request.POST['offerprice']
        offertill = offertill + " " + offertil
        
        if count <= 4:
            if realprice > offerprice:
                add_offer = Premium.objects.create(months=months, real_price=realprice, offer_price=offerprice, offer_till=offertill)
                add_offer.save()
                msg = "Added Successfully"
            else:
                msg = "Real Price Lesser Than OfferPrice is not acceptable"
        else:
            msg = "Maximum Number Of Packages Can Be Added Is 4"
    return render(request, "adminpremium.html", {'msg': msg, 'data': packages})

def admin_premium_delete(request):
    pid = request.GET['pid']
    premium = Premium.objects.get(id=pid)
    premium.delete()
    return redirect('/admin_premium')

def textsummary(request):
    abs_sum = ""
    ext_sum = ""
    if request.POST:
        text = request.POST['inputtext']
        nltk.download('punkt')
        nltk.download('stopwords')
        words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        stop_words = set(stopwords.words('english'))  # Define stopwords
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
        word_freq = Counter(filtered_words)
        top_words = [word for word, _ in word_freq.most_common(5)]  # Top 5 important words
        sentences = sent_tokenize(text)  # Tokenize the text into sentences
        summary_sentences = []
        for sentence in sentences:
            words_in_sentence = word_tokenize(sentence.lower())
            if any(word in words_in_sentence for word in top_words):
                summary_sentences.append(sentence)
        extractive_summary = " ".join(summary_sentences)
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        abstractive_summary = summarizer(extractive_summary, max_length=100, min_length=30, do_sample=False)
        print("Extractive Summary:")
        print(extractive_summary)
        ext_sum = extractive_summary
        print("\nAbstractive Summary:")
        print(abstractive_summary[0]['summary_text'])
        abs_sum = abstractive_summary[0]['summary_text']
    return render(request, "textsummary.html", {'summary': abs_sum})

def newspage(request):
    txt_summary = ""
    user = User.objects.get(loginid__id=request.session.get('uid'))
    data = []
    genre = ""
    page = request.session.get('page', 0)  
    try:
        news = News.objects.get(Q(title__icontains="") & Q(uid=user))
    except:
        news = None
    # Get user's preferred topics
    topic = News.objects.filter(Q(uid=user) & (Q(likes=1) | Q(timing__gte=20))).values_list('genre', flat=True)
    topic_list = Counter(topic)
    sorted_topic_list = dict(topic_list.most_common())
    # Fetch news based on search or preferred genre
    if request.POST:
        search = request.POST.get('search', '')
        response = rs.get(f'https://newsapi.org/v2/everything?q={search}&apiKey=d8d7834030fb4b2f949807cced7919cc', params={'pageSize': 100})
    elif len(sorted_topic_list) > 0:
        genre = list(sorted_topic_list.keys())[0]
        response = rs.get(f'https://newsapi.org/v2/everything?q={genre}&apiKey=d8d7834030fb4b2f949807cced7919cc', params={'pageSize': 100})
    else:
        response = rs.get('https://newsapi.org/v2/everything?q=india&apiKey=d8d7834030fb4b2f949807cced7919cc', params={'pageSize': 100})
    # Fetch common news
    common_response = rs.get('https://newsapi.org/v2/everything?q=india&apiKey=d8d7834030fb4b2f949807cced7919cc', params={'pageSize': 100})
    common_data = common_response.json().get('articles', [])
    data.extend(common_data)
    # Process the main response
    if response.status_code == 200:
        data = response.json().get('articles', [])
    else:
        print('Failed to fetch data:', response.status_code)
    # Handle GET request (skipping news)
    if request.GET:
        screen = int(request.GET.get('screen_time', 0))
        title = request.GET.get('genre', '')
        page += 1
        if page >= len(data):
            page = 0
        request.session['page'] = page
        url = data[page]['title'].split(" ")
        genre = random.choice([word for word in url if len(word) > 5])
        news, created = News.objects.get_or_create(title=title, uid=user, defaults={'genre': genre, 'timing': screen})
        if not created:
            news.timing = screen
            news.genre = genre
            news.save()
    print(page, "---------------")
    likes = News.objects.filter(Q(likes=1) & Q(title__icontains=data[page]['title'])).count()
    txt_summary = text_summary(data[page]['content'])['abstractive']
    tts = gTTS(text=txt_summary, lang='en', slow=False)
    media_dir = os.path.join(settings.BASE_DIR, 'static', 'media')
    os.makedirs(media_dir, exist_ok=True)
    tts.save(os.path.join(media_dir, "output.mp3"))
    
    translator = Translator()
    tger = translator.translate(txt_summary, src='en', dest='de').text
    tts = gTTS(text=tger, lang='de', slow=False) 
    tts.save(os.path.join(media_dir, "output_de.mp3"))

    tfr = translator.translate(txt_summary, src='en', dest='fr').text
    tts = gTTS(text=tfr, lang='fr', slow=False) 
    tts.save(os.path.join(media_dir, "output_fr.mp3"))

    thi = translator.translate(txt_summary, src='en', dest='hi').text
    tts = gTTS(text=thi, lang='hi', slow=False) 
    tts.save(os.path.join(media_dir, "output_hi.mp3"))

    return render(request, "news.html", {"p": data[page], "likes": likes, "genre": genre, "news": news, "txt_summary": txt_summary, 'tger': tger, 'tfr': tfr, 'thi': thi})

def like(request):
    title = request.GET['title']
    timing = request.GET.get('timing', 0)
    genre = request.GET['genre']
    if not timing:
        timing = 0
    user = User.objects.get(loginid__id=request.session.get('uid'))
    like = News.objects.filter(Q(title=title) & Q(uid=user)).exists()
    if like:
        news = News.objects.get(Q(title=title) & Q(uid=user))
        if news.likes == 0:
            news.likes = 1
        else:
            news.likes = 0
        news.save()
    else:
        news = News.objects.create(uid=user, genre=genre, timing=timing, title=title, likes=1)
        news.save()
    return redirect('/news')

# -------------------------------
# NEW: Voice Command Integration
# -------------------------------

def voice_command(request):
    """
    Renders a page with a voice command interface.
    (Not used when auto-triggered on homepage)
    """
    return render(request, "voice_command.html")

@csrf_exempt
def process_voice_command(request):
    """
    Processes the spoken command sent from the client.
    Depending on the command, returns a JSON response indicating the action.
    """
    if request.method == "POST":
        command = request.POST.get("command", "").lower()
        if "summarize news" in command or "read news" in command:
            response = {"action": "redirect", "url": "/news"}
        elif "go to home" in command:
            response = {"action": "redirect", "url": "/userhome"}
        elif "logout" in command:
            response = {"action": "redirect", "url": "/login"}
        else:
            response = {"action": "none", "message": "Command not recognized."}
        return JsonResponse(response)
    return JsonResponse({"action": "none", "message": "Invalid request."})
