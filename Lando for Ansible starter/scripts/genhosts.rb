#!/usr/bin/env ruby

require 'yaml'

hosts_file = YAML.load_file('hosts.yml')

templates = hosts_file[:templates]
hosts = hosts_file[:hosts]
groups = {}

out = ""

out += "[all]\n"
hosts.each do |host, host_data|
    data = host_data
    data['groups'].each do |group|
        groups[group] = [] unless groups.has_key?(group)
        groups[group] << host
    end if data.has_key?('groups')
    data.delete('groups')

    out += "#{host} #{data.map{|k,v| "#{k}=#{v}"}.join(' ')}\n"
end
out += "\n"

groups.each do |group, hosts|
    out += "[grp_#{group}]\n"
    out += hosts.join("\n")
    out += "\n\n"
end

output = File.open('hosts', 'w')
output.write(out)
output.close
