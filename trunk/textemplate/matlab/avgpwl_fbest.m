function fbest = avgpwl_fbest(x,Abar,bbar,NSAMPLES)
%
[m,n] = size(Abar);

sigma_A = sqrt(5);
sigma_b = sqrt(5);

Rbar = Abar*x + bbar;
ADelta = sigma_A/sqrt(m)*randn([m*NSAMPLES n]);
bDelta = sigma_b/sqrt(m)*randn([m NSAMPLES]);

F = Rbar*ones(1,NSAMPLES) + reshape(ADelta*x,m,NSAMPLES) + bDelta;
fbest = 1/NSAMPLES*( sum( max(F) ) );
