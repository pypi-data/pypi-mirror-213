#ifndef DLL_API
#define DLL_API extern "C" __declspec(dllimport)
#endif

void setcompremap(const char* file);

double masscom(double speed, double pi,int num);

double effcom(double speed, double pi,int num);

void setturmap(const char* file,double pt,double Tt,int maptype);

double masstur(double speed, double pi, int num);

double efftur(double speed, double pi, int num);

void setcompremapavi(const char* file,double speedscale,double massscale,double prscale,double effscale);

void setturmapavi(const char* file, double speedscale, double massscale, double prscale, double effscale);

double mapspeed(double mass, double pi,unsigned int num);

double mapeff(double mass, double pi, unsigned int num);

double turmappi(double W, double speed, unsigned int num);
