clear; clc;

cond = {'b1',...
    'r1','r2','r3','r1r3','r1r2','r2r3','r1r2r3',...
    'l1','l2','l3','l1l3','l1l2','l2l3','l1l2l3',...
    't1','t2','t3','t1t3','t1t2','t2t3','t1t2t3',...
    };
for m = 1: length(cond)
    file = cell2mat(cond(1,m));
    data = load(sprintf('D:/Atik/Data/Blade Data/data_20150516_20hz/%s_20hz_16.mat',file));
    data = data.Channel_003;

    dir = sprintf('D:/Aug/%s/SNR',file);

    snr = -8:2:10;
    for k = 1:length(snr)
        mkdir(sprintf('%s/%d dB',dir,snr(1,k)));
        testDir = sprintf('%s/%d dB',dir,snr(1,k));
        fprintf('Dir= %s\n', testDir);
        j = 150001;
        for i = 301:400
            y = data(j:j+499, :);
            out = agn(y,snr(1,k));
            scalogram(out,testDir,i);
            j = j+500;
        end
    end
end