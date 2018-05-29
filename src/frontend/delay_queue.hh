/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#ifndef DELAY_QUEUE_HH
#define DELAY_QUEUE_HH

#include <iostream>
#include <queue>
#include <cstdint>
#include <string>
#include <unordered_map>

#include "file_descriptor.hh"

struct pair_comp {
    bool operator()(const std::pair<uint64_t, std::string> &a, const std::pair<uint64_t, std::string> &b){
        return a.first > b.first;
    }
};
class DelayQueue
{
private:
    uint64_t delay_ms_;
    std::priority_queue< std::pair<uint64_t, std::string>, std::vector<std::pair<uint64_t, std::string>>, pair_comp> packet_queue_;
    std::unordered_map<std::string, float>ip_delays;
    /* release timestamp, contents */

public:
    DelayQueue( const uint64_t & s_delay_ms, const std::unordered_map<std::string, float>& delays) 
    : delay_ms_( s_delay_ms ), packet_queue_(), ip_delays(delays){}

    void read_packet( const std::string & contents );

    void write_packets( FileDescriptor & fd );

    unsigned int wait_time( void ) const;

    bool pending_output( void ) const { return wait_time() <= 0; }

    static bool finished( void ) { return false; }
};

#endif /* DELAY_QUEUE_HH */
