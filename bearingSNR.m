clear; clc;

cond = ["Norm",...
         "IR07", "IR14", "IR21",...
         "OR07", "OR14", "OR21",...
         "BF07", "BF14", "BF21"];
for m = 9: length(cond)
    data = load(sprintf('D:/Bearing Data/%s.mat',cond(1,m)));
    data = struct2cell(data);
    data = data{1,1};

    dir = sprintf('D:/Aug/Bearing/%s/SNR',cond(1,m));

    snr = -8:2:10;
    for k = 1:length(snr)
        mkdir(sprintf('%s/%d dB',dir,snr(1,k)));
        testDir = sprintf('%s/%d dB',dir,snr(1,k));
        fprintf('Dir= %s\n', testDir);
        j = 1;
        for i = 1:50
            y = data(j:j+599, :);
            out = agn(y,snr(1,k));
            scalogram(out,testDir,i);
            j = j+600;
        end
    end
end