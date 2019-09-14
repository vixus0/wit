#!/usr/bin/env ruby

require 'yaml'
require 'net/http'
require 'uri'

def api(endpoint)
  uri = URI.join(URI('https://hackathon.clue.co.uk/team6/api/v2/'), endpoint)

  puts "GET #{uri}"

  req = Net::HTTP::Get.new(uri).tap { |req|
      req['API_USER'] = 'superapi'
      req['API_KEY'] = '67B4FB9063984E0CAB32A7DFEE5F6745'
  }

  res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
    http.request(req)
  end

  res.body
end

spec = YAML.load_file('clue_openapi.yaml')

spec['paths'].keys.map { |k| k.split('/')[1] }.uniq.each do |path|
  puts path
  File.write(File.join('data', "#{path}.json"), api(path))
end
