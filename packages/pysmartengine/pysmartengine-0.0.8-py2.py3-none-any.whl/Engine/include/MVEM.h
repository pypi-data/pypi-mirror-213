void initengine(double Bore, double Stroke, double CR, double length, unsigned int numofcylindersin);

void MVEMstartnewcycle(double speed);

void MVEMcompress(double pimin, double Timin, double Tr, double xr, double kc, double phic, double ivcpcoeff);

void MVEMburn(double Rp, double etaloss, double fuelmass, double comdurcoeff);

void MVEMexpanse(double ke);

void MVEMgasexchange(double pem);

void MVEMsetvalvetiming(double intakeopen, double intakeclose, double exhaustopen, double exhaustclose);

void MVEMendcycle(double eatc);

double MVEMBMEP();

double MVEMIMEP();

double MVEMPMEP();

double MVEMPower();

double MVEMBSFC();

double MVEMairflow();

double MVEMetit();

double MVEMalpha();

void MVEMsetvalvetiming(double intakeopen, double intakeclose, double exhaustopen, double exhaustclose);

double MVEMTt(double etav);

void MVEMcylinderpressure(const char* filename);

void MVEMcompressure(const char* filename);

double MVEMpmax();

double MVEMTmax();