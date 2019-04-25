no_of_users = 5;

no_of_channels = 5;

Tsf = 2 + 2*(no_of_channels - 1);

total_time = 600000;

time_elapsed = 0;

sample_count = ones(no_of_users,no_of_channels);

%observed_mean

assignments = zeros(no_of_users);%line changed 

flags = zeros(no_of_users);

reward_distribution =  [
 0.4 0.1 0.5 0.4 0.2;
 0.9 0.2 0.7 0.4 0.1;
 0.2 0.4 0.2 0.4 0.1;
 0.75 0.6 0.2 0.1 0.4;
 0.1 0.7 0.5 0.3 0.6];

epsilon = 1/number_of_channels;
initiator = -1;
responder = -1;
preference = -1;

function is_super_frame = beginning_of_SF(t, Tsf)
    if(rem(t, Tsf) == 1)
        is_super_frame = true;
    else
        is_super_frame = false;
    end
end

function ucb_indices = calculate_ucb_indices(observed_mean, sample_count, t, no_of_users, no_of_channels)
    ucb_indices = zeros(no_of_users,no_of_channels);
    for i = 1 : no_of_users
        for j = 1 : no_of_channels
            ucb_indices(i, j) = observed_mean(i, j) + sqrt((2*log(t))/sample_count(i, j));
        end
    end
end


function preferred_channels = find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels)
    preferred_channels = zeros(no_of_users,no_of_channels);
    for i = 1 : no_of_users
        for j = 1 : no_of_channels
            counter = 1;
            if( ucb_indices(i, j) > ucb_indices(i)(assignments(i)))
                preferred_channels(i, counter) = j;
                counter = counter + 1;
            end
        end
    end
end


function ucb_indices, preferred_channels = rank_channels(assignments, observed_mean, sample_count, t, number_of_users, number_of_channels)
    ucb_indices = calculate_UCB_indices(observed_mean, sample_count, t, number_of_users, number_of_channels);
    preferred_channels = find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels);
end



function flag = calculate_flag(epsilon)
    if (rand(0, 1) >= epsilon * 10)
        flag = 0;
    else
        flag = 1;
    end
end

function owner =  owner(channel, assignments):
    owner = -1;
    for 1:(length(assignments))
        if (assignments(i) == channel):
            owner =  i;
        end
    end
end

function response =  propose_swap(responder, ucb_indices, initiator, assignments)
    if responder == -1
        response = 1;
    if ucb_indices(responder, assignments(initiator)) > ucb_indices(responder, assignments(responder)
        response = 0;
    else
        response = 0;
    end
end



% incomplete
function rewards =  execute_actions(assignments, reward_distribution, initiator, responder, t, Tsf, number_of_users, number_of_channels):
        if (beginning_of_SF(t, Tsf))
            rewards = []
        for i in range(number_of_users):
            if (i != initiator and i != responder):
                instantanious_reward = bernoulli_reward.find_reward(reward_distribution[i][assignments[i]])
            else:
                instantanious_reward = -1
            rewards.append(instantanious_reward)
        return rewards



% incomplete
function find_initiator(flags, number_of_users)
    for i in range(len(flags)):
        if (flags[i] == 1):
            return i
    else:
        return 0






            



    
