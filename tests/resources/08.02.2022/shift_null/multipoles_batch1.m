% FIRST STEP
% RUN SHIMS 3 'first mag-run-number'
file_number=1;
% PROCESS VERTICAL FIELDS
system('copy param_by_ds.par param.par')   
%system('copy mult1by-U48.par param.par');   
%system('D:\programs\shims\shims.exe 5 1');    
for nn = 1:file_number;
   dat_name =  ['mult' int2str(nn) 'by' '.dvm'] 
   f = fopen('DATA.dat','w');
   fprintf(f,dat_name);
   fclose(f);
   system('D:\programs\analyze\analyze.exe');
end 
 
% PROCESS HORIZONTAL FIELDS
system('copy param_bz_ds.par param.par');   
%system('copy mult1bz-U48.par param.par');
%system('D:\programs\shims\shims.exe 5 2');    
for nn = 1:file_number;
   dat_name =  ['mult' int2str(nn) 'bz' '.dvm'] 
   f = fopen('DATA.dat','w');
   fprintf(f,dat_name);
   fclose(f);
   system('D:\programs\analyze\analyze.exe');
end 
 











