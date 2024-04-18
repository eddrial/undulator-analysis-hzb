irun_a = 8200;            
irun_b = 8203;
irun_c = 8206;
title_a = 'Z = 10.0 mm';
title_b = 'Z = 17.5 mm';
title_c = 'Z = 25.0 mm';
print_name = ['mag_field_plus_z.png']; 

% irun_a = 8192;            
% irun_b = 8189;
% irun_c = 8186;
% title_a = 'Z = -10.0 mm';
% title_b = 'Z = -17.5 mm';
% title_c = 'Z = -25.0 mm';
% print_name = ['mag_field_minus_z.png']; 


hall_cal_by = importdata('y_calib_senis112_17.spl');
sz=size(hall_cal_by);
senis_volt_by   = hall_cal_by(1:sz(1),1);
senis_mag_by    = hall_cal_by(1:sz(1),2);

hall_cal_bz = importdata('z_calib_senis112_17.spl');
sz=size(hall_cal_bz);
senis_volt_bz   = hall_cal_bz(1:sz(1),1);
senis_mag_bz    = hall_cal_bz(1:sz(1),2);


filename0 =  ['MAG' int2str(irun_a) '.DVM'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
z0   = A(1,1:sz(2));
by0  = A(2,1:sz(2));
bz0  = A(3,1:sz(2));
by_a = spline(senis_volt_by,senis_mag_by,by0);
bz_a = spline(senis_volt_bz,senis_mag_bz,bz0);

filename0 =  ['MAG' int2str(irun_b) '.DVM'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
z0   = A(1,1:sz(2));
by0  = A(2,1:sz(2));
bz0  = A(3,1:sz(2));
by_b = spline(senis_volt_by,senis_mag_by,by0);
bz_b = spline(senis_volt_bz,senis_mag_bz,bz0);

filename0 =  ['MAG' int2str(irun_c) '.DVM'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
z0   = A(1,1:sz(2));
by0  = A(2,1:sz(2));
bz0  = A(3,1:sz(2));
by_c = spline(senis_volt_by,senis_mag_by,by0);
bz_c = spline(senis_volt_bz,senis_mag_bz,bz0);


pic1=figure;
xmin = 850.0;
xmax = 2750.0;
yymin = -0.5;
yymax =  0.5;
yzmin = -0.16;
yzmax =  0.16;



%-----------------A------------------------
subplot(3,2,1);
plot( z0 , by_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('BY [T]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yymin,yymax]),
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,2);
plot( z0 , bz_a,'b');
title(title_a);
xlabel('X coordinate  [mm]');
ylabel('BZ [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%-----------------B------------------------
subplot(3,2,3);
plot( z0 , by_a,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('BY [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yymin,yymax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,4);
plot( z0 , bz_b,'b');
title(title_b);
xlabel('X coordinate  [mm]');
ylabel('BZ [T]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%--------------------C---------------------
subplot(3,2,5);
plot( z0 , by_c,'b');
title(title_c);
xlabel('X coordinate  [mm]');
ylabel('BY [T]');
set (gca,'XLim',[xmin,xmax]);
set (gca,'YLim',[yymin,yymax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(3,2,6);
plot( z0 , bz_c,'b');
title(title_c);
xlabel('X coordinate  [mm]');
ylabel('BZ [T]');
set (gca,'XLim',[xmin,xmax]),
set (gca,'YLim',[yzmin,yzmax]);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;
print(pic1,'-dpng','-r600',print_name);
