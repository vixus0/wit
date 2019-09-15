#!/usr/bin/env ruby

require 'json'
require 'yaml'
require 'net/http'
require 'uri'

def api(endpoint)
  uri = URI.join('https://hackathon.clue.co.uk/team6/api/v2/', endpoint)

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

  items = []

  loop do
    data = JSON.load(api(path))
    new_items = data&.dig('_embedded', 'items')
    items.push(*new_items) unless new_items.nil?
    next_href = data&.dig('_links', 'next', 'href')
    next_href.nil? ? break : path = next_href[1..]
  end

  puts items.size 
  path = path.split('?')[0]

  File.write(File.join('data', "#{path}.json"), JSON.dump({ 'items' => items }))
end
