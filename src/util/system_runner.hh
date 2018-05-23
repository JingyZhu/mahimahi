#ifndef SYSTEM_RUNNER_HH
#define SYSTEM_RUNNER_HH

#include <vector>
#include <string>
#include <functional>

int ezexec( const std::vector< std::string > & command, const bool path_search = false, const bool redirect = false, std::string filename = "");
void run( const std::vector< std::string > & command, const bool path_search = false);

#endif /* SYSTEM_RUNNER_HH */
