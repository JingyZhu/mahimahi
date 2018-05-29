/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <sstream>
#include <fstream>

#include "delay_queue.hh"
#include "util.hh"
#include "ezio.hh"
#include "packetshell.cc"

using namespace std;

static void read_delays(string directory, unordered_map<string, float>& ip_delays){
    ifstream in(directory + "/traffic.txt");
    if (!in.good()) throw runtime_error(directory + "traffic.txt not exists");
    string line, ip;
    float delay;
    while(getline(in, line)) {
        istringstream is(line);
        is >> ip >> delay;
        ip_delays[ip] = delay * 1000;
    }
    return;
}

int main( int argc, char *argv[] )
{
    try {
        /* clear environment while running as root */
        char ** const user_environment = environ;
        environ = nullptr;

        check_requirements( argc, argv );

        if ( argc < 2 ) {
            throw runtime_error( "Usage: " + string( argv[ 0 ] ) + " delay-milliseconds [RTT file] -- [command...]" );
        }

        const uint64_t delay_ms = myatoi( argv[ 1 ] );

        vector< string > command;
        string directory;
        unordered_map<string, float> ip_delays;

        if ( argc == 2 ) {
            command.push_back( shell_path() );
        } else {
            int i = 2;
            if (string(argv[i]) != "--"){
                directory = string(argv[2]);
                read_delays(directory, ip_delays);
                i++;
            }
            for (++i; i < argc; i++ ) {
                command.push_back( argv[ i ] );
            }
            if (command.empty())
                command.push_back(shell_path());
        }

        PacketShell<DelayQueue> delay_shell_app( "delay", user_environment);

        delay_shell_app.start_uplink( "[delay " + to_string( delay_ms ) + " ms] ",
                                      command, 
                                      delay_ms, ip_delays);
        delay_shell_app.start_downlink( delay_ms, ip_delays);
        return delay_shell_app.wait_for_exit();
    } catch ( const exception & e ) {
        print_exception( e );
        return EXIT_FAILURE;
    }
}
