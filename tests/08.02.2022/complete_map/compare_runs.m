irun0 = 7286;            %warm 
irun1 = 7350;            %6mm
irun2 = 7334;            %7mm
irun3 = 7318;            %10mm
irun4 = 7302;            %15mm
irun5 = 7382;            %20mm

print_name = ['cpmu17_cool_down.png']; 

no_iterations         = 4;

filename0 =  ['mittel_' int2str(irun0) '_' int2str(irun0+no_iterations-1) '.dat'];  
f_sp0 = fopen(filename0);
A=fscanf(f_spl,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
z0   = A(1,1:sz(2));
by0  = A(2,1:sz(2));
bz0  = A(3,1:sz(2));

filename1 =  ['mittel_' int2str(irun1) '_' int2str(irun1+no_iterations-1) '.dat'];  
f_spl = fopen(filename1);
A=fscanf(f_spl,'%f %f %f',[3 inf]);
fclose(f_spl);
sz=size(A);
z1   = A(1,1:sz(2));
by1  = A(2,1:sz(2));
bz1  = A(3,1:sz(2));

filename2 =  ['mittel_' int2str(irun2) '_' int2str(irun2+no_iterations-1) '.dat'];  
f_sp2 = fopen(filename2);
A=fscanf(f_sp2,'%f %f %f',[3 inf]);
fclose(f_sp2);
sz=size(A);
z2   = A(1,1:sz(2));
by2  = A(2,1:sz(2));
bz2  = A(3,1:sz(2));

filename3 =  ['mittel_' int2str(irun3) '_' int2str(irun3+no_iterations-1) '.dat'];  
f_sp3 = fopen(filename3);
A=fscanf(f_sp3,'%f %f %f',[3 inf]);
fclose(f_sp3);
sz=size(A);
z3   = A(1,1:sz(2));
by3  = A(2,1:sz(2));
bz3  = A(3,1:sz(2));

filename4 =  ['mittel_' int2str(irun4) '_' int2str(irun4+no_iterations-1) '.dat'];  
f_sp4 = fopen(filename4);
A=fscanf(f_sp4,'%f %f %f',[3 inf]);
fclose(f_sp4);
sz=size(A);
z4   = A(1,1:sz(2));
by4  = A(2,1:sz(2));
bz4  = A(3,1:sz(2));

filename5 =  ['mittel_' int2str(irun5) '_' int2str(irun5+no_iterations-1) '.dat'];  
f_sp5 = fopen(filename5);
A=fscanf(f_sp5,'%f %f %f',[3 inf]);
fclose(f_sp5);
sz=size(A);
z5   = A(1,1:sz(2));
by5  = A(2,1:sz(2));
bz5  = A(3,1:sz(2));

fsize=10.0;
myfont = 'normal';

pic1=figure;
subplot(2,1,1);
plot(z0,bz0,'k+');
hold on ;
plot(z1,bz1,'r.');
plot(z1,bz2,'b');
plot(z1,bz3,'g');
plot(z1,bz4,'c.');
plot(z1,bz5,'y');
legend('5.5mm(warm)','6mm','7mm','10mm','15mm','20mm');
xlabel('position [mm]','FontSize',fsize,'FontWeight',myfont);
ylabel('hor. field integral BZ [Tmm]','FontSize',fsize,'FontWeight',myfont);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
set (gca,'Fontsize',fsize,'FontWeight',myfont,'XLim',[-20.,20.]),

subplot(2,1,2);
plot(z0,by0,'k+');
hold on ;
plot(z1,by1,'r.');
plot(z1,by2,'b');
plot(z1,by3,'g');
plot(z1,by4,'c.');
plot(z1,by5,'y');
legend('5.5mm(warm)','6mm','7mm','10mm','15mm','20mm');
xlabel('position [mm]','FontSize',fsize,'FontWeight',myfont);
ylabel('vertical field integral BY [Tmm]','FontSize',fsize,'FontWeight',myfont);
set (gca,'XGrid','on');
set (gca,'YGrid','on');
set (gca,'Fontsize',fsize,'FontWeight',myfont,'XLim',[-20.,20.]),

print(pic1,'-dpng','-r600',print_name); 

