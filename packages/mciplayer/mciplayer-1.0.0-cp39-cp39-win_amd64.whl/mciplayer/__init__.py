"""
Main module of mciplayer.
Defines MCIPlayer class which records and plays audio (mp3,wav,mid).
"""
from ._mciwnd import *
from .tool import MCIError,SupportError,mciplayermethod
import os
from uuid import uuid4
class MCIPlayer():
    @mciplayermethod
    def __init__(self,filename=None):
        """
        Creates a player instance
        If filename is given, it will create a player which has opened the given filename,otherwise it will create a player not opening anything.
        """
        if filename is None:
            self.wnd=MCIWndCreateNull(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG)
        else:
            self.wnd=MCIWndCreate(0,0,WS_POPUP+MCIWNDF_NOPLAYBAR+MCIWNDF_NOERRORDLG,filename.encode('ansi'))
        self._audios=[]
        self._names=[]
    @mciplayermethod
    def play(self):
        """
        Starts playing audio opened by the player
        """
        if not MCIWndCanPlay(self.wnd):
            raise SupportError('Play is unsupported for this MCI Window')
        MCIWndPlay(self.wnd)
    @mciplayermethod
    def pause(self):
        """
        Pauses playing audio opened by the player
        """
        MCIWndPause(self.wnd)
    @mciplayermethod
    def resume(self):
        """
        Resumes paused audio opened by the player
        """
        MCIWndResume(self.wnd)
    @mciplayermethod
    def close(self):
        """
        Closes the player.
        """
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
        return MCIWndGetPosition(self.wnd)
    @mciplayermethod
    def start(self):
        """
        Returns an integer which stands for the start of the audio (in milliseconds).
        """
        return MCIWndGetStart(self.wnd)
    @mciplayermethod
    def end(self):
        """
        Returns an integer which stands for the end of the audio (in milliseconds).
        """
        return MCIWndGetEnd(self.wnd)
    @mciplayermethod
    def length(self):
        """
        Returns the length of the audio (in milliseconds).
        It is also possible to use self.start()-self.end() to get the same thing.
        """
        return MCIWndGetLength(self.wnd)
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
        MCIWndSave(self.wnd,b'a')
        self._audios.append(dn)
        os.chdir(cwd)
        self._names.append(os.path.abspath(filename))
    @mciplayermethod
    def open(self,fn):
        """
        Open a new audio file
        """
        MCIWndOpen(self.wnd,fn.encode('ansi'),0)
    @mciplayermethod
    def enable_record(self):
        """
        Enables recording.
        """
        MCIWndNew(self.wnd,b'waveaudio')
    @mciplayermethod
    def start_record(self):
        """
        Starts recording.
        """
        if not MCIWndCanRecord(self.wnd):
            raise SupportError('Record is unsupported for this MCI Window')
        MCIWndRecord(self.wnd)
    @mciplayermethod
    def tostart(self):
        """
        Moves the player to the start of the audio.
        """
        MCIWndHome(self.wnd)
    @mciplayermethod
    def toend(self):
        """
        Move the player to the end of the audio.
        """
        MCIWndEnd(self.wnd)
    @mciplayermethod
    def stop(self):
        """
        Stops ths player.
        """
        MCIWndStop(self.wnd)
    @mciplayermethod
    def topos(self,pos):
        """
        Moves the player to a given position.
        """
        MCIWndSeek(self,pos)
    @mciplayermethod
    def volume(self):
        """
        Gets the volume of the player.
        """
        return MCIWndGetVolume(self.wnd)
    @mciplayermethod
    def setvolume(self,vol):
        """
        Set the volume of the player.
        """
        MCIWndSetVolume(self.wnd,vol)
    @mciplayermethod
    def speed(self):
        """
        Gets the speed of the player.
        """
        return MCIWndGetSpeed(self.wnd)
    @mciplayermethod
    def setspeed(self,speed):
        """
        Sets the speed of the player.
        """
        return MCIWndSetSpeed(self.wnd,speed)
    @mciplayermethod
    def wait(self):
        """
        Waits until the player finishes playing current audio.
        """
        while self.position()<self.end():
            pass
    def __del__(self):
        self.close()
__all__=['MCIPlayer']