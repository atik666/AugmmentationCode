clear; clc;

normal = load ('D:\OneDrive - ump.edu.my\Atik_Home\Data Files\Bearing Data Center\Normal Baseline Data\97.mat');

path = 'D:/OneDrive - ump.edu.my/Atik_Home/Writing/Augmentation/Data';
trainDir = sprintf('%s/%s/Train',path,file);
augDir = sprintf('%s/%s/Aug',path,file);
valDir = sprintf('%s/%s/Val',path,file);
testDir = sprintf('%s/%s/Test',path,file);

NstdMax = 0.2; NstdMin = 0.1; j =1;
for i = 1 : 400
    if i <= 200
        y = data(j:j+499, :);
        scalogram(y,trainDir,i);
        j = j+ 500;
        
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
        y11 = sum(y11,2)/100;
        y22 = cell2mat(y2);
        y22 = sum(y22,2)/100;
        z = (y11+y22)/2;
        scalogram(z,augDir,i);
    elseif i >= 201 && i <= 300
         y = data(j:j+499, :);
         scalogram(y,valDir,i);
         j = j+ 500;
    elseif i >= 301 && i <= 400
         y = data(j:j+499, :);
         scalogram(y,testDir,i);
         j = j+ 500;
    end
end
