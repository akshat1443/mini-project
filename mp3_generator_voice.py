import time
from gtts import gTTS
import os
import subprocess
from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
import sqlite3
import sys
import pyfingerprint
import time
import hashlib
from  pyfingerprint import PyFingerprint

tts = gTTS('alert    someone is waiting outside ', lang='en') 
tts.save('positionnumber000.mp3')
