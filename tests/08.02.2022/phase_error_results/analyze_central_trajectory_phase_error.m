
irun_a =  1;            

% title_a = 'mag.field (central) (Z = 0. mm)';
% title_b = 'first mag.field integral (Z = 0. mm)';
mtitle_s0   = '\color{red} SHIFT = 0 mm  ';
mtitle_s14  = '\color{red} SHIFT = 14 mm  ';
mtitle_s28  = '\color{red} SHIFT = 28 mm';
mtitle_m14  = '\color{red} SHIFT = -14 mm  ';
mtitle_m28  = '\color{red} SHIFT = -28 mm  ';

ymin = -10;
ymax =  10;

print_name = 'pha_error.png'; 
% 



% --------------------shift 0 -------------------------------
filename0 =  ['mult0by.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_pha_0   = A(2,1:sz(2));

filename0 =  ['mult0bz.pha'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_pha_0   = A(2,1:sz(2));

% -----------------shift 14 ----------------------------------
filename0 =  ['mult14by.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x14     = A(1,1:sz(2));
by_pha_14   = A(2,1:sz(2));

filename0 =  ['mult14bz.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x14     = A(1,1:sz(2));
bz_pha_14   = A(2,1:sz(2));

%-----------------shift -14 ----------------------------------
filename0 =  ['mult_m14by.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
xm14     = A(1,1:sz(2));
by_pha_m14   = A(2,1:sz(2));

filename0 =  ['mult_m14bz.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
xm14     = A(1,1:sz(2));
bz_pha_m14   = A(2,1:sz(2));

% ---------------shift 28 ------------------------------------
filename0 =  ['mult28by.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x28     = A(1,1:sz(2));
by_pha_28   = A(2,1:sz(2));

filename0 =  ['mult28bz.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x28     = A(1,1:sz(2));
bz_pha_28   = A(2,1:sz(2));


% ---------------shift -28 ------------------------------------
filename0 =  ['mult_m28by.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
xm28            = A(1,1:sz(2));
by_pha_m28   = A(2,1:sz(2));

filename0 =  ['mult_m28bz.pha']
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
xm28     = A(1,1:sz(2));
bz_pha_m28   = A(2,1:sz(2));

% 

pic1=figure;


% 28mm
subplot(5,2,1);
plot( x28 , by_pha_28*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BY PHA [grd]');
title('\color{red} SHIFT = 28 mm');
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(5,2,2);
plot( x28 , bz_pha_28*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BZ PHA [grd]');
title(mtitle_s28);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

% shift 14
subplot(5,2,3);
plot( x14 , by_pha_14*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BY PHA [grd]');
title(mtitle_s14);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(5,2,4);
plot( x14 , bz_pha_14*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BZ PHA [grd]');
title(mtitle_s14);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

% shift 0
subplot(5,2,5);
plot( x0 , by_pha_0*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BY PHA [grd]');
title(mtitle_s0);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(5,2,6);
plot( x0 , bz_pha_0*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BZ PHA [grd]');
title(mtitle_s0);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

% shift -14
subplot(5,2,7);
plot( xm14 , by_pha_m14*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BY PHA [grd]');
title(mtitle_m14);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(5,2,8);
plot( xm14 , bz_pha_m14*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BZ PHA [grd]');
title(mtitle_m14);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

% shift -28
subplot(5,2,9);
plot( xm28 , by_pha_m28*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BY PHA [grd]');
title(mtitle_m28);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(5,2,10);
plot( xm28 , bz_pha_m28*360,'b');% 
set (gca,'YLim',[ymin,ymax]),
xlabel('X coordinate  [mm]');
ylabel('BZ PHA [grd]');
title(mtitle_m28);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;



print(pic1,'-dpng','-r600',print_name);

% 
% %-----------------A------------------------
% subplot(2,2,1);
% plot( x0 , by_a,'b');
% title(title_a);
% xlabel('X coordinate  [mm]');
% ylabel('BY [T]');
% set (gca,'XLim',[xmin,xmax]),
% set (gca,'YLim',[ymin,ymax]),
% set (gca,'XGrid','on');
% set (gca,'YGrid','on');
% grid on;
% 
% subplot(2,2,2);
% plot( x0 , bz_a,'b');
% title(title_a);
% xlabel('X coordinate  [mm]');
% ylabel('BZ [T]');
% set (gca,'XLim',[xmin,xmax]);
% set (gca,'YLim',[-0.1,0.1]);
% set (gca,'XGrid','on');
% set (gca,'YGrid','on');
% grid on;
% 
% %----------------integral------------------------
% subplot(2,2,3);
% plot( x0 , Iby_b,'b');
% title(title_b);
% xlabel('X coordinate  [mm]');
% ylabel('IBYdx [Tmm]');
% set (gca,'XLim',[xmin,xmax]),
% set (gca,'YLim',[yymin,yymax]),
% set (gca,'XGrid','on');
% set (gca,'YGrid','on');
% grid on;
% 
% subplot(2,2,4);
% plot( x0 , Ibz_b,'b');
% title(title_b);
% xlabel('X coordinate  [mm]');
% ylabel('IBZdx [Tmm]');
% set (gca,'XLim',[xmin,xmax]);
% set (gca,'YLim',[yzmin,yzmax]);
% set (gca,'XGrid','on');
% set (gca,'YGrid','on');
% grid on;
% 
% 
% 
% print(pic1,'-dpng','-r600',print_name);
