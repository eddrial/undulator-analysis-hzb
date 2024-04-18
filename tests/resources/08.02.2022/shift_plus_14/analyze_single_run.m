irun0 = 8189;            


%print_name = ['cpmu17_cool_down.png']; 



filename0 =  ['MAG' int2str(irun0) '.DVM'];  
f_sp0 = fopen(filename0);
A=fscanf(f_sp0,'%f %f %f',[3 inf]);
fclose(f_sp0);
sz=size(A);
z0   = A(1,1:sz(2));
by0  = A(2,1:sz(2));
bz0  = A(3,1:sz(2));

dz = zeros(sz(2)-1);

for i = 1:sz(2)-1
    dz(i) = z0(i+1)-z0(i);
end
figure;
%plot( z0(2:sz(2)) , dz,'.');


plot( z0 , bz0,'.');
title(filename0);

figure
plot( z0 , by0,'.');
title(filename0);