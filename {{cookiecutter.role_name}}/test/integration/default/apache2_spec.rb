describe package('apache2') do
it { should be_installed }
end

describe port(80) do
it { should be_listening }
its('processes') {should eq ['apache2']}
end
