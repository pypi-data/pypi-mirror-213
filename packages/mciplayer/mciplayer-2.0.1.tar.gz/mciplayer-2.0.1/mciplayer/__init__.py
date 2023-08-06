"""
Main module of mciplayer.
Defines MCIPlayer class which records and plays audio (mp3,wav,wmv,etc. ).
"""
from ._mciwnd import *
from .tool import MCIError,SupportError,mciplayermethod
import os
from uuid import uuid4
from argparse import *
from ._mciwnd_unicode import * # UTF-8 Support
class MCIPlayer():
    @mciplayermethod
    def __init__(self,filename=None,use_utf8=True):
        """
        Creates a player instance
        If filename is given, it will create a player which has opened the given filename,otherwise it will create a player not opening anything.
        UTF-8 support has been added now, and the use_utf8 argument controls whether to use UTF-8 or not.
        """
        if filename is None:
            if use_utf8:
                self.wnd=uMCIWndCreateNull(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG)
            else:
                self.wnd=MCIWndCreateNull(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG)
        else:
            if use_utf8:
                self.wnd=uMCIWndCreate(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG,filename.encode('utf-8'))
            else:
                self.wnd=MCIWndCreate(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG,filename.encode('ansi'))
        self._audios=[]
        self._names=[]
        self.use_utf8=use_utf8
    @mciplayermethod
    def play(self):
        """
        Starts playing audio opened by the player
        """
        if not MCIWndCanPlay(self.wnd):
            raise SupportError('Play is unsupported for this MCI Window')
        if self.use_utf8:
            uMCIWndPlay(self.wnd)
        else:
            MCIWndPlay(self.wnd)
    @mciplayermethod
    def pause(self):
        """
        Pauses playing audio opened by the player
        """
        if self.use_utf8:
            uMCIWndPause(self.wnd)
        else:
            MCIWndPause(self.wnd)
    @mciplayermethod
    def resume(self):
        """
        Resumes paused audio opened by the player
        """
        if self.use_utf8:
            uMCIWndResume(self.wnd)
        else:
            MCIWndResume(self.wnd)
    @mciplayermethod
    def close(self):
        """
        Closes the player.
        """
        if self.use_utf8:
            uMCIWndClose(self.wnd)
        else:
            MCIWndClose(self.wnd)
        cwd=os.getcwd()
        os.chdir(os.environ['TMP'])
        for i in range(len(self._audios)):
            with open('./'+self._audios[i]+'/a','rb') as f:
                c=f.read()
            with open(self._names[i],'wb') as f:
                f.write(c)
        os.chdir(cwd)


    @mciplayermethod
    def position(self):
        """
        Returns an integer which stands for the position of the audio the player is playing currently (in milliseconds).
        """
        return MCIWndGetPosition(self.wnd) if not self.use_utf8 else uMCIWndGetPosition(self.wnd)
    @mciplayermethod
    def start(self):
        """
        Returns an integer which stands for the start of the audio (in milliseconds).
        """
        return MCIWndGetStart(self.wnd) if not self.use_utf8 else uMCIWndGetStart(self.wnd)
    @mciplayermethod
    def end(self):
        """
        Returns an integer which stands for the end of the audio (in milliseconds).
        """
        return MCIWndGetEnd(self.wnd) if not self.use_utf8 else uMCIWndGetEnd(self.wnd)
    @mciplayermethod
    def length(self):
        """
        Returns the length of the audio (in milliseconds).
        It is also possible to use self.start()-self.end() to get the same thing.
        """
        return MCIWndGetLength(self.wnd) if not self.use_utf8 else uMCIWndGetLength(self.wnd)
    @mciplayermethod
    def save(self,filename):
        """
        Saves the audio in the player.
        """
        if not MCIWndCanSave(self.wnd):
            raise SupportError('Save is unsupported for this MCI Window')
        if not filename.endswith('.wav'):
            raise SupportError('save() supports only wave audio.')
        cwd=os.getcwd()
        os.chdir(os.environ['TMP'])
        dn=str(uuid4())
        os.mkdir(dn)
        os.chdir(dn)
        if self.use_utf8:
            uMCIWndSave(self.wnd,b'a')
        else:
            MCIWndSave(self.wnd,b'a')
        self._audios.append(dn)
        os.chdir(cwd)
        self._names.append(os.path.abspath(filename))
    @mciplayermethod
    def open(self,fn):
        """
        Open a new audio file
        """
        if self.use_utf8:
            uMCIWndOpen(self.wnd,fn.encode('utf-8'),0)
        else:
            MCIWndOpen(self.wnd,fn.encode('ansi'),0)
    @mciplayermethod
    def enable_record(self):
        """
        Enables recording.
        """
        if self.use_utf8:
            uMCIWndNew(self.wnd,b'waveaudio')
        else:
            MCIWndNew(self.wnd,b'waveaudio')
    @mciplayermethod
    def start_record(self):
        """
        Starts recording.
        """
        if not MCIWndCanRecord(self.wnd):
            raise SupportError('Record is unsupported for this MCI Window')
        if self.use_utf8:
            uMCIWndRecord(self.wnd)
        else:
            MCIWndRecord(self.wnd)
    @mciplayermethod
    def tostart(self):
        """
        Moves the player to the start of the audio.
        """
        if self.use_utf8:
            uMCIWndHome(self.wnd)
        else:
            MCIWndHome(self.wnd)
    @mciplayermethod
    def toend(self):
        """
        Move the player to the end of the audio.
        """
        if self.use_utf8:
            uMCIWndEnd(self.wnd)
        else:
            MCIWndEnd(self.wnd)
    @mciplayermethod
    def stop(self):
        """
        Stops ths player.
        """
        if self.use_utf8:
            uMCIWndStop(self.wnd)
        else:
            MCIWndStop(self.wnd)
    @mciplayermethod
    def topos(self,pos):
        """
        Moves the player to a given position.
        """
        if self.use_utf8:
            uMCIWndSeek(self.wnd,pos)
        else:
            MCIWndSeek(self.wnd,pos)
    @mciplayermethod
    def volume(self):
        """
        Gets the volume of the player.
        """
        return MCIWndGetVolume(self.wnd) if not self.use_utf8 else uMCIWndGetVolume(self.wnd)
    @mciplayermethod
    def setvolume(self,vol):
        """
        Set the volume of the player.
        """
        if self.use_utf8:
            uMCIWndSetVolume(self.wnd,vol)
        else:
            MCIWndSetVolume(self.wnd,vol)
    @mciplayermethod
    def speed(self):
        """
        Gets the speed of the player.
        """
        return MCIWndGetSpeed(self.wnd) if not self.use_utf8 else uMCIWndGetSpeed(self.wnd)
    @mciplayermethod
    def setspeed(self,speed):
        """
        Sets the speed of the player.
        """
        return MCIWndSetSpeed(self.wnd,speed) if not self.use_utf8 else uMCIWndSetSpeed(self.wnd,speed)
    @mciplayermethod
    def wait(self):
        """
        Waits until the player finishes playing current audio.
        """
        while self.position()<self.end():
            pass
    def __del__(self):
        """
        Close the player before deletion.
        """
        self.close()
def _play_demo():
    """
    Demostration for playing.
    """
    a=ArgumentParser()
    a.add_argument('audio_name',help='Input audio file name')
    p=a.parse_args()
    player=MCIPlayer(p.audio_name) # Create player instance.
    player.play() # Play audio.
    player.wait() # Wait for the audio ends.
def _record_demo():
    """
    Demostration for recording.
    """
    a=ArgumentParser()
    a.add_argument('audio_name',help='Output audio file name.')
    a.add_argument('record_secs',help='Number of seconds to record.')
    p=a.parse_args()
    player=MCIPlayer() # Create player instance.
    player.enable_record() # Enable recording.
    player.start_record() # Record.
    __import__('time').sleep(float(p.record_secs)) # Wait.
    player.save(p.audio_name)
__all__=['MCIPlayer','MCIError','SupportError']