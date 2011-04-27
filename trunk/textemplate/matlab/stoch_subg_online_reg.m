% On-line learning and regression example via stochastic subgradients.
%
% EE364b Convex Optimization II, S. Boyd
% Written by Almir Mutapcic, 01/19/07
% 
PRINT_PLOTS = 0; % save eps files with generated plots

n = 10; % number of weights (variables)

% generate a random Sigma_x covariance matrix
randn('state',1); % set state so it is reproducable
S = randn(n,n);
Sigma_x = S'*S;

% linear relationship
a = randn(n,1)/sqrt(n);
Sigma_y = a'*Sigma_x*a + 0.1;
Sigma_xy = Sigma_x*a;

Sigma = [Sigma_x, Sigma_xy; Sigma_xy', Sigma_y];
R = sqrtm(Sigma);

%********************************************************************
% run stochastic subgradient method with diminishing step sizes
%********************************************************************
f = [+Inf]; fbest = [+Inf]; errors = [+Inf];

MAX_ITERS = 5000; 

% initial point
w_1 = zeros(n,1);

iter = 1;
w = w_1;
whist = [w];

while iter < MAX_ITERS 
  if( rem(iter,500) == 0 ), fprintf(1,'iter: %d\n',iter), end

  % generate a new sample from the distribution
  z = R*randn([n+1 1]); 
  x = z(1:n);  y = z(n+1);

  % noisy subgradient calculation
  e = w'*x - y;
  g = sign(e)*x;

  % step size selection
  alpha = 1/iter;

  % objective values
  errors(end+1) = e;
  fval = abs(e);
  f(end+1) = fval;
  fbest(end+1) = min( fval, fbest(end) );

  % subgradient update
  w = w - alpha*g; iter = iter + 1; whist = [whist, w];
end

w_sign = w;

%********************************************************************
% compute optimal weight that minimizes mean-square error
% (use the analytic formula and the stochastic subgradient method)
%********************************************************************
f_lms = [+Inf]; fbest_lms = [+Inf]; errors_lms = [+Inf];

MAX_ITERS = 5000; 

% analytical solution
w_formula = Sigma(1:n,1:n)\Sigma(1:n,n+1);

iter = 1;
w = w_formula;

while iter < MAX_ITERS 
  if( rem(iter,500) == 0 ), fprintf(1,'iter: %d\n',iter), end

  % generate a new sample from the distribution
  z = R*randn([n+1 1]); 
  x = z(1:n);  y = z(n+1);

  % noisy subgradient calculation
  e = w'*x - y;
  g = 2*e*x;

  % step size selection
  alpha = 0.1/iter;

  % objective values
  errors_lms(end+1) = e;
  fval_lms = abs(e);
  f_lms(end+1) = fval_lms;
  fbest_lms(end+1) = min( fval_lms, fbest_lms(end) );

  % subgradient update
  w = w - alpha/norm(g)*g; iter = iter + 1;
end

w_lms = w;

%********************************************************************
% plots
%********************************************************************
% generate random samples
NSAMPLES = 1000;
Z = R*randn([n+1 NSAMPLES]); 
X = Z(1:n,:);  Y = Z(n+1,:);

err_sign = ( w_sign'*X - Y );
abserr_sign = abs( err_sign );

err_lms    = ( w_lms'*X - Y );
abserr_lms = abs( err_lms );

err_form    = ( w_formula'*X - Y );
abserr_form = abs( err_form );

disp(' ')
fprintf(1,'Sign abs predict error %3.4f\n',mean(abs(err_sign)));
fprintf(1,'Sign mean-square error %3.4f\n',mean((err_sign).^2));
disp(' ')
fprintf(1,'LMS  abs predict error %3.4f\n',mean(abs(err_lms)));
fprintf(1,'LMS  mean-square error %3.4f\n',mean((err_lms).^2));
disp(' ')
fprintf(1,'Form abs predict error %3.4f\n',mean(abs(err_form)));
fprintf(1,'Form mean-square error %3.4f\n',mean((err_form).^2));

iters = [1:MAX_ITERS];
figure(1), clf
set(gca, 'FontSize',18);
plot( iters, errors, 'b-','LineWidth', 1 )
axis([1 300 -40 40])
xlabel('k');
ylabel('pred error');
if( PRINT_PLOTS ), print -depsc online_reg_errors, end

% histogram plots
edges = linspace(-2,2,40);
[count_1] = histc( err_sign, edges )';
[count_2] = histc( err_lms,  edges )';
common_axis = [-2 2 0 150];

figure(2), clf
% stoch distribution
bar( edges, count_1, 'histc' ); hold on,
hline = findobj(gca,'Type','line'); delete(hline)
hpatch = findobj(gca,'Type','patch');
set(hpatch,'FaceColor',[0.91,0.91,0.91])
set(gca, 'FontSize',16);
hold off,
axis([common_axis])
title('sign')
if( PRINT_PLOTS ), print -depsc online_reg_dist, end

figure(3), clf
% stoch distribution
subplot(2,1,1), bar( edges, count_1, 'histc' ); hold on,
hline = findobj(gca,'Type','line'); delete(hline)
hpatch = findobj(gca,'Type','patch');
set(hpatch,'FaceColor',[0.91,0.91,0.91])
set(gca, 'FontSize',16);
hold off,
axis([common_axis])
title('sign')

% optimal lms distribution
subplot(2,1,2), bar( edges, count_2, 'histc' ); hold on,
hline = findobj(gca,'Type','line'); delete(hline)
hpatch = findobj(gca,'Type','patch');
set(hpatch,'FaceColor',[0.91,0.91,0.91])
set(gca, 'FontSize',16);
hold off,
axis([common_axis])
title('lms')
