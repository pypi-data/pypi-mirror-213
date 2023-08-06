#ifndef UNICODE//Support Unicode
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#include<windows.h>
#include<pybind11/pybind11.h>
#include<vfw.h>
#include<string>
#include<utility>
#pragma comment(lib,"vfw32.lib")
#pragma comment(lib,"user32.lib")
namespace py = pybind11;
using namespace std;
int mwc(
    int hwndParent,
    int hInstance,
    unsigned dwStyle,
    py::bytes szFile
) {
    string s(szFile);
    wchar_t* dst = new wchar_t[1000];
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), 1000, dst, 1000);
    return (int)MCIWndCreate((HWND)hwndParent, (HINSTANCE)hInstance, dwStyle, dst);
}
int mwp(int hwnd) {
    return (int)MCIWndPlay((HWND)hwnd);
}
int mwp_(int hwnd) {
    return (int)MCIWndPause((HWND)hwnd);
}
int mwr(int hwnd) {
    return (int)MCIWndResume((HWND)hwnd);
}
int mwgs(int hwnd) {
    return (int)MCIWndGetStart((HWND)hwnd);
}
int mwge(int hwnd) {
    return (int)MCIWndGetEnd((HWND)hwnd);
}
int mwgp(int hwnd) {
    return (int)MCIWndGetPosition((HWND)hwnd);
}
int mwgl(int hwnd) {
    return (int)MCIWndGetLength((HWND)hwnd);
}
int mwh(int hwnd) {
    return (int)MCIWndHome((HWND)hwnd);
}
int mwe(int hwnd) {
    return (int)MCIWndEnd((HWND)hwnd);
}
int mwrc(int hwnd) {
    return (int)MCIWndRecord((HWND)hwnd);
}
int mwss(int hwnd, int speed) {
    return (int)MCIWndSetSpeed((HWND)hwnd, speed);
}
int mwgsp(int hwnd) {
    return (int)MCIWndGetSpeed((HWND)hwnd);
}
bool mwcp(int hwnd) {
    return MCIWndCanPlay((HWND)hwnd);
}
bool mwcr(int hwnd) {
    return MCIWndCanRecord((HWND)hwnd);
}
int mwsv(int hwnd, int vol) {
    return MCIWndSetVolume((HWND)hwnd, vol);
}
int mwgv(int hwnd) {
    return MCIWndGetVolume((HWND)hwnd);
}
int mwsvf(int hwnd, py::bytes file) {
    string f(file);
    wchar_t* dst = new wchar_t[1000];
    MultiByteToWideChar(CP_UTF8, 0, f.c_str(), 1000, dst, 1000);
    return MCIWndSave((HWND)hwnd, dst);
}
bool mwcs(int hwnd) {
    return MCIWndCanSave((HWND)hwnd);
}
int mwsk(int hwnd, int pos) {
    return MCIWndSeek((HWND)hwnd, pos);
}
int mwo(int hwnd, py::bytes file, int f) {
    string fn(file);
    wchar_t* dst = new wchar_t[1000];
    MultiByteToWideChar(CP_UTF8, 0, fn.c_str(), 1000, dst, 1000);
    return MCIWndOpen((HWND)hwnd, dst, f);
}
int mwn(int hwnd, py::bytes tp) {
    string s(tp);
    wchar_t* dst = new wchar_t[1000];
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), 1000, dst, 1000);
    return MCIWndNew((HWND)hwnd, dst);
}
pair<int, py::bytes> mwer(int hwnd) {
    wchar_t* error = new wchar_t[1000];
    int er = MCIWndGetError((HWND)hwnd, error, 1000);
    char* tmp = new char[1000];
    WideCharToMultiByte(CP_UTF8, 0, error, 1000, tmp, 1000, 0, 0);
    string str(tmp);
    delete[] error;
    delete[] tmp;
    return make_pair(er, py::bytes(str));
}
int mwcl(int hwnd) {
    return MCIWndClose((HWND)hwnd);
}
int mwcn(
    int hwndParent,
    int hInstance,
    unsigned dwStyle
) {
    return (int)MCIWndCreate((HWND)hwndParent, (HINSTANCE)hInstance, dwStyle, 0);
}
int mwt(int hwnd) {
    return MCIWndStop((HWND)hwnd);
}
PYBIND11_MODULE(_mciwnd_unicode, m) {
    m.def("uMCIWndCreate", &mwc);
    m.def("uMCIWndCreateNull", &mwcn);
    m.def("uMCIWndPlay", &mwp);
    m.def("uMCIWndPause", &mwp_);
    m.def("uMCIWndResume", &mwr);
    m.def("uMCIWndGetStart", &mwgs);
    m.def("uMCIWndGetEnd", &mwge);
    m.def("uMCIWndGetPosition", &mwgp);
    m.def("uMCIWndGetLength", &mwgl);
    m.def("uMCIWndHome", &mwh);
    m.def("uMCIWndEnd", &mwe);
    m.def("uMCIWndRecord", &mwrc);
    m.def("uMCIWndSetSpeed", &mwss);
    m.def("uMCIWndGetSpeed", &mwgsp);
    m.def("uMCIWndCanPlay", &mwcp);
    m.def("uMCIWndCanRecord", &mwcr);
    m.def("uMCIWndSetVolume", &mwsv);
    m.def("uMCIWndGetVolume", &mwgv);
    m.def("uMCIWndSave", &mwsvf);
    m.def("uMCIWndCanSave", &mwcs);
    m.def("uMCIWndSeek", &mwsk);
    m.def("uMCIWndOpen", &mwo);
    m.def("uMCIWndGetError", &mwer);
    m.def("uMCIWndClose", &mwcl);
    m.def("uMCIWndNew", &mwn);
    m.def("uMCIWndStop", &mwt);
    m.attr("WS_OVERLAPPED") = 0x00000000L;
    m.attr("WS_POPUP") = 0x80000000L;
    m.attr("WS_CHILD") = 0x40000000L;
    m.attr("WS_MINIMIZE") = 0x20000000L;
    m.attr("WS_VISIBLE") = 0x10000000L;
    m.attr("WS_DISABLED") = 0x08000000L;
    m.attr("WS_CLIPSIBLINGS") = 0x04000000L;
    m.attr("WS_CLIPCHILDREN") = 0x02000000L;
    m.attr("WS_MAXIMIZE") = 0x01000000L;
    m.attr("WS_CAPTION") = 0x00C00000L;
    m.attr("WS_BORDER") = 0x00800000L;
    m.attr("WS_DLGFRAME") = 0x00400000L;
    m.attr("WS_VSCROLL") = 0x00200000L;
    m.attr("WS_HSCROLL") = 0x00100000L;
    m.attr("WS_SYSMENU") = 0x00080000L;
    m.attr("WS_THICKFRAME") = 0x00040000L;
    m.attr("WS_GROUP") = 0x00020000L;
    m.attr("WS_TABSTOP") = 0x00010000L;
    m.attr("WS_MINIMIZEBOX") = 0x00020000L;
    m.attr("WS_MAXIMIZEBOX") = 0x00010000L;
    m.attr("MCIWNDF_NOAUTOSIZEWINDOW") = 0x0001;
    m.attr("MCIWNDF_NOPLAYBAR") = 0x0002;
    m.attr("MCIWNDF_NOAUTOSIZEMOVIE") = 0x0004;
    m.attr("MCIWNDF_NOMENU") = 0x0008;
    m.attr("MCIWNDF_SHOWNAME") = 0x0010;
    m.attr("MCIWNDF_SHOWPOS") = 0x0020;
    m.attr("MCIWNDF_SHOWMODE") = 0x0040;
    m.attr("MCIWNDF_SHOWALL") = 0x0070;
    m.attr("MCIWNDF_NOTIFYMODE") = 0x0100;
    m.attr("MCIWNDF_NOTIFYPOS") = 0x0200;
    m.attr("MCIWNDF_NOTIFYSIZE") = 0x0400;
    m.attr("MCIWNDF_NOTIFYERROR") = 0x1000;
    m.attr("MCIWNDF_NOTIFYALL") = 0x1F00;
    m.attr("MCIWNDF_NOTIFYANSI") = 0x0080;
    m.attr("MCIWNDF_RECORD") = 0x2000;
    m.attr("MCIWNDF_NOERRORDLG") = 0x4000;
}