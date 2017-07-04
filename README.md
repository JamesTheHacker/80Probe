# 80Probe

80Probe was developed by [@JamesTheHaxor](http://twitter.com/JamesTheHaxor) to brute force subdomains to test for active webservers. If you participate in bug bounty programs you'll find this script super helpful.

## How It Works

Traditionally the way to brute force subdomains is to use something like [dnsrecon](https://github.com/darkoperator/dnsrecon) (great tool btw that I use daily). But, this doesn't give you any indication whether the subdomain is hosting a webserver. If you're not interested in knowing whether the subdomain has a webserver this tool will be usless to you.

80Probe takes in a list of subdomains and tests each one to see if it's running a webserver. I make use of multithreading to test multiple subdomains at once. If the webserver returns content when testing port 80 the subdomain is up :)

**Speed Note**

This method is slow because it makes a HTTP request to every subdomain. Depending on your connection it may take a couple of minutes to test 1000 subdomains. I run 80Probe on Digital Ocean servers as they have faster connections than I do.

## Usage

![80Probe Example Usage](http://i.imgur.com/bSBmLpq.png "80Probe Example Usage")

Requirements:

* `pip install requests`
* `pip install argparse`

Example usage:

    80probe.py --domain google.com --wordlist ./subdomains-1000.txt --filter "dnserror"

* `--domain/-d`: Domain name to scan. Do not include a subdomain!
* `--wordlist/-w`: Path to the wordlist file containing the subdomains (one subdomain per line)
* `--filter/-f`: (optional) Removes subdomains that contain filter text in the HTTP response
* `--showBody/-s`: (optional) Useful for debugging (see below)
* `--timeout/-t`: Number of seconds to wait before HTTP request times out

Upon completion 80Probe will return a list all subdomains that have active webservers. These can be piped into other tools, or saved to a file.

**Important: ISP DNS Wildcards**

[Most ISP's use DNS wildcards](https://en.wikipedia.org/wiki/Wildcard_DNS_record#Registries.2FISPs). This means if you enter a non existant domain name your ISP will return one of their own pages. These are usually search pages, or pages filled with ads. Believe it or not ISP's make a lot of money from this as they're able to serve ads and get paid for the impressions.

To test if your ISP is doing this simply visit this URL: [http://this-subdomain-does-not-exist.google.com](http://this-subdomain-does-not-exist.google.com). If you see page from your ISP they're using wildcards. If your ISP uses wildcards this is bad because 80Probe will include lots of false positives. We don't want that.

To get around this I've included a `--filter` argument. What this does is checks the body of every HTTP response. If it contains the filter word/s it is removed. By doing this you can be 99% positive the active subdomains are actually up!

In my case my ISP returns a page that contains the word `dnserror`. I filter that out so any page that contains the word `dnserror` is not included in the results.

## Author Notes

What I tend to do is run dnsrecon to get a list of subdomains, save the results as `.csv` and pipe the subdomains into 80Probe. This saves on the requests and speeds up the process. I have a few personal gripes with dnsreacon. It doesn't filter out wildcard results. There is a `-f` option, but it doesn't work. This makes automation difficult.

## Contributions

If you can make this script better, or improve any issues, submit a pull request and I will happily merge :)