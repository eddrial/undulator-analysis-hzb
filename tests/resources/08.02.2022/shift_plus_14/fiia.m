% SECOND INTEGRAL FIELD MAP
NFILES = 1;
centre = round(NFILES/2);
%FIRST RUN NUMBER (for graphic file output)
first_run =  2021650;

%PLOT IBydx
zstep = 2.5;
zstart= -30.0;
zz=zeros(NFILES,1);
for i = 1:NFILES
    zz(i)= zstart+(i-1)*zstep;
end

last_run = first_run + NFILES -1;
print_name = ['fiia_' int2str(first_run) '_' int2str(last_run) '.pdf'];
print_named = ['fiia_' int2str(first_run) '_' int2str(last_run) '.png'];
title_name =  ['RUN: ' int2str(first_run) ' - ' int2str(last_run)];

%define PLOT YRANGE in Tmm^2
ymin = -1000.;
ymax =  1000;
%define space between plot lines
line_space=100.;

% search for data array dimensions
nn = 1;
dat_by =  ['mult' int2str(nn) 'by' '.siii'];
fy = fopen(dat_by,'r');
BYY=fscanf(fy,'%f %f',[2 inf]);
sy=size(BYY);
sz = sy;
fclose(fy);

xy = zeros(NFILES,sy(2));
by = zeros(NFILES,sy(2));
xz = zeros(NFILES,sz(2));
bz = zeros(NFILES,sz(2));


for nn = 1:NFILES;
   dat_by =  ['mult' int2str(nn) 'by' '.sii']; 
   dat_bz =  ['mult' int2str(nn) 'bz' '.sii']; 
  
   fy = fopen(dat_by,'r');
   BYY=fscanf(fy,'%f %f',[2 inf]);
   xy(nn,1:sy(2))=BYY(1,1:sy(2));
   by(nn,1:sy(2))=BYY(2,1:sy(2));
   
   fz = fopen(dat_bz,'r');
   BZZ=fscanf(fz,'%f %f',[2 inf]);
   xz(nn,1:sz(2))=BZZ(1,1:sz(2));
   bz(nn,1:sz(2))=BZZ(2,1:sz(2));
   
   fclose(fy);
   fclose(fz);
end

pic1=figure;


%PLOT IBydx
subplot(2,2,1);
hold on;

zero_ref = by(centre,1)+line_space*centre;

for nn = 1:NFILES;
    if nn == centre
        line_width = 2.;
        line_color = 'r';
    else
        line_width = 0.5;
        line_color = 'black';
    end
    plot(xy(nn,1:sy(2)),-zero_ref+nn*line_space+by(nn,1:sy(2)),line_color,'LineWidth',line_width);
    
end
set (gca,'XLim',[0,max(xy(1,1:sy(2)))]);
%set (gca,'YLim',[ymin,ymax]);
xlabel('x / mm');
ylabel('IBydx  / Tmm^2');
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;
title(title_name);

%PLOT IBzdx
subplot(2,2,2);
hold on;

zero_ref = bz(centre,1)+line_space*centre;

for nn = 1:NFILES;
    if nn == centre
        line_width = 2.;
        line_color = 'r';
    else
        line_width = 0.5;
        line_color = 'black';
    end
    plot(xz(nn,1:sz(2)),-zero_ref+nn*line_space+bz(nn,1:sz(2)),line_color,'LineWidth',line_width);
    
end
set (gca,'XLim',[0,max(xz(1,1:sz(2)))]);
%set (gca,'YLim',[ymin,ymax]);
xlabel('x / mm');
ylabel('IBzdx  / Tmm^2');
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;


subplot(2,2,3);
plot(zz,by(1:NFILES,sy(2)),line_color);
set (gca,'XLim',[min(zz),max(zz)]);
%set (gca,'YLim',[ymin,ymax]);
xlabel('z / mm');
ylabel('IBydx  / Tmm^2');
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

subplot(2,2,4);
plot(zz,bz(1:NFILES,sz(2)),line_color);
set (gca,'XLim',[min(zz),max(zz)]);
%set (gca,'YLim',[ymin,ymax]);
xlabel('z / mm');
ylabel('IBzdx  / Tmm^2');
set (gca,'XGrid','on');
set (gca,'YGrid','on');
grid on;

%print(pic1,'-dpdf','-r600',print_name); 
print(pic1,'-dpng','-r600',print_named);
fdat = fopen('mult_byzii_matlab.dat','w');
for i=1:NFILES;
    fprintf(fdat,'%10.4f %10.4f %10.4f\n',zz(i),by(i,sy(2)),bz(i,sz(2)) );
end
fclose(fdat);   


