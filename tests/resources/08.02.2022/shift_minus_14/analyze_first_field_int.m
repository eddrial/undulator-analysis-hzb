% irun_a = 21;            
% irun_b = 24;
% irun_c = 27;
% title_a = 'first mag.field integral (Z = 10.0 mm)';
% title_b = 'first mag.field integral (Z = 17.5 mm)';
% title_c = 'first mag.field integral (Z = 25.0 mm)';
% print_name = ['mag_field_integral_plus_z.png']; 

irun_a =  7;            
irun_b = 10;
irun_c = 13;
title_a = 'first mag.field integral (Z = -10.0 mm)';
title_b = 'first mag.field integral (Z = -17.5 mm)';
title_c = 'first mag.field integral (Z = -25.0 mm)';
print_name = ['mag_field_integral_minus_z.png']; 


% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_a) 'by.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_a   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_a) 'bz.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_a   = A(2,1:sz(2));


% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_b) 'by.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_b   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_b) 'bz.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_b   = A(2,1:sz(2));

% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_c) 'by.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_c   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_c) 'bz.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_c   = A(2,1:sz(2));

% 
% 
pic1=figure;
xmin = 850.0;
xmax = 2750.0;
yymin = -2.;
yymax =  2.;
yzmin = -1.;
yzmax =  1.;
% 
% 
% 
%-----------------A------------------------
subplot(3,2,1);
plot( x0 , by_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('IBYdx [Tmm]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yymin,yymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,2);
plot( x0 , bz_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('IBZdx [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%-----------------B------------------------
subplot(3,2,3);
plot( x0 , by_b,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('IBYdx [Tmm]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yymin,yymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,4);
plot( x0 , bz_b,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('IBZdx [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%-----------------C------------------------
subplot(3,2,5);
plot( x0 , by_c,'b');
title(title_c);
xlabel('X coordinate  [mm]');
ylabel('IBYdx [Tmm]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yymin,yymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,6);
plot( x0 , bz_c,'b');
title(title_c);
xlabel('X coordinate  [mm]');
ylabel('IBZdx [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


print(pic1,'-dpng','-r600',print_name);
