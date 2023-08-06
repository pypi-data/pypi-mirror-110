/* TEMPLATE.H
 *
 * This is the header file which defines the interface of the template.
 * Includes functions for loading and defining simulation parameters.
 */

#include "model.h"

namespace Gillespy
{
	extern std::vector<unsigned int> species_populations;
	extern std::vector<std::string> species_names;
	extern std::vector<std::string> reaction_names;

	double map_propensity(int reaction_id, const std::vector<int> &state);
	double map_propensity(int reaction_id, unsigned int *S);
	double map_ode_propensity(int reaction_id, const std::vector<double> &state);
	void add_reactions(Model &model);

	void map_variable_parameters(std::stringstream &stream);
	void map_variable_populations(std::stringstream &stream);
}
