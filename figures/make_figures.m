filenames = ["Reward", "Action", "Kill"];
average_length = 50;
for index = 1:length(filenames)
    figure()
    y = dlmread([char(filenames(index)), '_statistics.txt']).';
    x = 1:length(y);
    avg = zeros(size(x));
    rolling_avg = zeros(size(x));
    for i = 1:length(y)
        avg(i) = mean(y(1:i));
    end
    
    for i = 1:average_length-1
        rolling_avg(i) = mean(y(1:i));
    end
    for i = average_length:length(y)
        rolling_avg(i) = mean(y(i-average_length+1:i));
    end
    c = ["black", "red", "blue"];
    
    l_raw = 'raw score';
    l_avg = 'mean';
    l_roll = [num2str(average_length), '-trial mean'];
    
    p_raw = plot(x,y,'.','color', char(c(1)));
    legend(l_raw);
    hold on
    p_avg = plot(x,avg,'DisplayName',l_avg, 'color', char(c(2)), 'LineWidth',2);
    p_roll = plot(x,rolling_avg,'DisplayName',l_roll, 'color', char(c(3)), 'LineWidth',2);
    hold off
    
    leg = legend(l_raw, l_avg, l_roll);
    
    
    xlabel('Trials')
    ylabel(char(filenames(index)))
    title(['Figure ', num2str(index)])
    print(char(filenames(index)), '-dpng')
end