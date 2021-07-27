clc; clear;

T = 1/40000;
t = 1/160:(0.05-1/160)/(40000*0.05):0.05;

% x1 = 1.5 .* 10.^(-800.*(t)) * sin(2*pi*5000.*t);
% x2 = 0.2*(1+cos(2*pi*100*t))*cos(2*pi*100*t);

for n = 1:2001
    x1{n} = 1.5 * 10.^(-800.*(t(n))) * sin(2*pi*5000*n);
    x2{n} = 0.2*(1+cos(2*pi*100*n)).*cos(2*pi*1000*n);
    x3{n} = cos(2*pi*0.05*(n - 1));
end

normal = load ('D:\OneDrive - ump.edu.my\Atik_Home\Data Files\Bearing Data Center\Normal Baseline Data\97.mat');
y = normal.X097_DE_time(1:600);

NstdMax = 0.2; NstdMin = 0.1;
for k = 1:100
    Nstd = (NstdMax-NstdMin).*rand(1,1) + NstdMin;
    x1 = randn(length(y),1); 
    x1 = x1 - mean(x1);
    x1 = x1 -std(x1);

    x2 = randn(length(y),1); 
    x2 = x2 - mean(x2);
    x2 = x2 -std(x2);
    
    y1{k} = y + (x1.*Nstd);
    y2{k} = y - (x2.*Nstd);
end 

y11 = cell2mat(y1);
y11 = sum(y11,2)/k;
y22 = cell2mat(y2);
y22 = sum(y22,2)/k;
z = (y11+y22)/2;

rms2 = rms(abs(sum(y)-sum(z)))./rms(z);

a = (1/length(y))*sum(z.^2);
b = (1/length(y))*sum(y.^2) - a;

        