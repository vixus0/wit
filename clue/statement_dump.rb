#!/usr/bin/env ruby

require 'json'
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

while (data = JSON.load(api('statements')))['_links']['next'] do
  data['_embedded']['items'].map { |item| item[''] }
  data = api(data['_links']['next']['href'])
end
