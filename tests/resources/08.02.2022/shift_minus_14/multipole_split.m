first_run_no = 599;            
file_number=1;


for nn = 1:file_number;
irun = first_run_no - 1 + nn;

filename0 =  ['MAG' int2str(irun) '.DVM']  
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
line_no = sz(2);
x   = A(1,1:sz(2));
by  = A(2,1:sz(2));
bz  = A(3,1:sz(2));

dat_by =  ['mult' int2str(nn) 'by' '.dvm']; 
dat_bz =  ['mult' int2str(nn) 'bz' '.dvm']; 

fby = fopen(dat_by,'w');
fbz = fopen(dat_bz,'w');

for i = 1:line_no
fprintf(fby,'%10.3f %10.5e\n',x(i),by(i));
fprintf(fbz,'%10.3f %10.5e\n',x(i),bz(i));   
end

fclose(fby);
fclose(fbz);

end