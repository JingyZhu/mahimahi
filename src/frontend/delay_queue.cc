/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <limits>
#include <cstring>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <linux/ip.h>

#include "delay_queue.hh"
#include "timestamp.hh"

using namespace std;

void DelayQueue::read_packet( const string & contents )
{
    string no_tun_contents = contents.substr(4);
 
    struct iphdr *iph = (struct iphdr *)no_tun_contents.c_str();
    struct sockaddr_in dest;
    memset(&dest, 0, sizeof(dest));
    dest.sin_addr.s_addr = iph->daddr;
    std::unordered_map<string, float>::iterator it =
        ip_delays.find(inet_ntoa(dest.sin_addr));
    float RTT_delay = 0;
    if (it != ip_delays.end()) {
        // mapping file times are in milliseconds
        // we add all delay on uplink because dest ip
        // on downlink is client ip (note that this shouldn't matter)
        RTT_delay = (it->second);
    }
    packet_queue_.emplace( timestamp() + delay_ms_ + int(RTT_delay/2), contents );
}

void DelayQueue::write_packets( FileDescriptor & fd )
{
    while ( (!packet_queue_.empty())
            && (packet_queue_.top().first <= timestamp()) ) {
        fd.write( packet_queue_.top().second );
        packet_queue_.pop();
    }
}

unsigned int DelayQueue::wait_time( void ) const
{
    if ( packet_queue_.empty() ) {
        return numeric_limits<uint16_t>::max();
    }

    const auto now = timestamp();

    if ( packet_queue_.top().first <= now ) {
        return 0;
    } else {
        return packet_queue_.top().first - now;
    }
}
