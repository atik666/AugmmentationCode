function noisySig = agn(sig,reqSNR)
sigEner = norm(sig(:))^2;                    % energy of the signal
noiseEner = sigEner/(10^(reqSNR/10));        % energy of noise to be added
noiseVar = noiseEner/(length(sig(:))-1);     % variance of noise to be added
noiseStd = sqrt(noiseVar);                   % std. deviation of noise to be added
noise = noiseStd*randn(size(sig));           % noise
noisySig = sig+noise;                        % noisy signal
end