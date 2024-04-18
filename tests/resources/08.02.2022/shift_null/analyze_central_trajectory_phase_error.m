
irun_a =  1;            

% title_a = 'mag.field (central) (Z = 0. mm)';
% title_b = 'first mag.field integral (Z = 0. mm)';
mtitle  = 'SHIFT = 0 mm  ';
print_name = 'pha_error.png'; 
% 

% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_a) 'by.sii'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
by_sii   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_a) 'bz.sii'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x0     = A(1,1:sz(2));
bz_sii   = A(2,1:sz(2));


% ---------------------------------------------------
filename0 =  ['mult' int2str(irun_a) 'by.pha'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x1     = A(1,1:sz(2));
by_pha   = A(2,1:sz(2));

filename0 =  ['mult' int2str(irun_a) 'bz.pha'];
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f',[2 inf]);
fclose(f_sp0);
sz=size(A);
x1     = A(1,1:sz(2));
bz_pha   = A(2,1:sz(2));


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
subplot(2,2,1);
plot( x0 , by_sii,'b');% 
xlabel('X coordinate  [mm]');
ylabel('BY SII');
title(mtitle);

subplot(2,2,2);
plot( x0 , bz_sii,'b');% 
xlabel('X coordinate  [mm]');
ylabel('BZ SII');
title(mtitle);

subplot(2,2,3);
plot(x1,by_pha*360,'b');% 
xlabel('X coordinate  [mm]');
ylabel('BY PHA');
title(mtitle);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(2,2,4);
plot(x1,bz_pha*360,'b');% 
xlabel('X coordinate  [mm]');
ylabel('BZ PHA');
title(mtitle);
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
