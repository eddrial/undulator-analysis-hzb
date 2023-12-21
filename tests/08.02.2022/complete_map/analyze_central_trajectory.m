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
title_a = 'mag.field (central) (Z = 0. mm)';
title_b = 'first mag.field integral (Z = 0. mm)';
title_c = 'first mag.field integral (Z = -25.0 mm)';
print_name = ['mag_field_central_traject.png']; 


% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_a) 'by.spl'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_a   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_a) 'bz.spl'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_a   = A(2,1:sz(2));


% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_a) 'by.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
Iby_b   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_a) 'bz.fli'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
Ibz_b   = A(2,1:sz(2));


% 
% 
pic1=figure;
xmin = 850.0;
xmax = 2750.0;
ymin = -0.5;
ymax =  0.5;
yzmin = -1.;
yzmax =  1.;
% 
% 
% 
%-----------------A------------------------
subplot(2,2,1);
plot( x0 , by_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('BY [T]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[ymin,ymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(2,2,2);
plot( x0 , bz_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('BZ [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[-0.1,0.1]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%----------------integral------------------------
subplot(2,2,3);
plot( x0 , Iby_b,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('IBYdx [Tmm]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yymin,yymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(2,2,4);
plot( x0 , Ibz_b,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('IBZdx [Tmm]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;



print(pic1,'-dpng','-r600',print_name);
