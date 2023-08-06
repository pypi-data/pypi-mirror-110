#include <exception>
#include <Teuchos_ParameterList.hpp>
#include <Teuchos_XMLParameterListHelpers.hpp>
#include "paramset.hpp"

namespace
{
using namespace Teuchos;

std::vector<std::string>
split_name(const std::string& param_name)
{
    std::string delimiter = "->";
    std::string name(param_name);
    std::vector<std::string> name_parts;

    size_t pos = 0;
    while ((pos = name.find(delimiter)) != std::string::npos) {
        name_parts.push_back(name.substr(0, pos));
        name.erase(0, pos + delimiter.length());
    }
    name_parts.push_back(name);

    return name_parts;
}

const Teuchos::ParameterList&
lookupNestedParameterList
(std::string& param, const Teuchos::ParameterList& params)
{
    std::vector<std::string> name_parts = split_name(param);
    param = name_parts.back();
    name_parts.pop_back();

    const ParameterList *list = &params;
    for (auto& key : name_parts) {
        list = &list->sublist(key);
    }

    return *list;
}

Teuchos::ParameterList&
lookupNestedParameterList(std::string& param, Teuchos::ParameterList& params)
{
    std::vector<std::string> name_parts = split_name(param);
    param = name_parts.back();
    name_parts.pop_back();

    ParameterList *list = &params;
    for (auto& key : name_parts) {
        list = &list->sublist(key);
    }

    return *list;
}
}

void
ParamSet::load_from_file(const std::string& path)
{
    auto loadedParams = getParametersFromXmlFile(path);
    loadedParams->validateParameters(defaultInitParams);
    parameters.setParameters(*loadedParams);
}

void
ParamSet::save_to_file(const std::string& path)
{ writeParameterListToXmlFile(parameters, path); }

Teuchos::ParameterList&
ParamSet::commit()
{
    committed = true;
    return parameters;
}

Teuchos::ParameterList&
ParamSet::updates()
{ return committed ? updatedParams : parameters; }

void
ParamSet::update_committed_parameters(Teuchos::ParameterList params)
{
    params.validateParameters(defaultInitParams);
    parameters.setParameters(params);
    updatedParams.setParameters(Teuchos::ParameterList());
}

void
ParamSet::reset()
{ parameters = defaultInitParams; }

int
ParamSet::get_num_params(const std::string& param_name)
{
    if (param_name.empty()) {
        return parameters.numParams();
    }

    ParameterEntry &param = get_param_entry(param_name);

    if (!param.isList()) return 0;

    return getValue<ParameterList>(param).numParams();
}

std::string
ParamSet::get_param_name(const std::string& param_name, int i)
{
    ParameterList::ConstIterator it;

    if (param_name.empty()) {
        it = parameters.begin();
    } else {
        ParameterEntry &param = get_param_entry(param_name);
        ParameterList &paramList = getValue<ParameterList>(param);
        it = paramList.begin();
    }

    std::advance(it, i);
    return it->first;
}

std::string
ParamSet::get_param_type(const std::string& param_name)
{
    const ParameterEntry &param = get_param_entry(param_name);
    try {
        return types.at(param.getAny().type());
    } catch (const std::out_of_range& exc) {
        return "unknown";
    }
}

ParameterEntry&
ParamSet::get_param_entry(const std::string& param_name)
{
    if (committed) {
        try {
            return get_param_entry(param_name, updatedParams);
        } catch (const Teuchos::Exceptions::InvalidParameterName& exc) {
            //Fallback to main parameter list
        }
    }

    return get_param_entry(param_name, parameters);
}

void
ParamSet::set_param_entry
(std::string param_name, Teuchos::ParameterEntry param)
{
    if (committed) {
        auto& resultList = lookupNestedParameterList(param_name, updatedParams);
        resultList.setEntry(param_name, param);
    } else {
        auto& resultList = lookupNestedParameterList(param_name, parameters);
        resultList.setEntry(param_name, param);
    }
}

ParameterEntry&
ParamSet::get_param_entry
(std::string param_name, Teuchos::ParameterList& params)
{
    auto& result = lookupNestedParameterList(param_name, params);

    return result.getEntry(param_name);
}

const ParameterEntry&
ParamSet::get_param_entry
(std::string param_name, const Teuchos::ParameterList& params)
{
    auto& result = lookupNestedParameterList(param_name, params);

    return result.getEntry(param_name);
}


void
ParamSet::throw_param_mismatch(const std::string& param_name)
{
    std::string msg = "Type mismatch for parameter: ";
    msg += param_name;

    throw std::runtime_error(msg);
}

void
ParamSet::throw_param_unsettable(const std::string& param_name)
{
    std::string msg = "Parameter not settable after committing: ";
    msg += param_name;

    throw std::runtime_error(msg);
}

const std::map<std::type_index,std::string>
ParamSet::types = {
    { std::type_index(typeid(ParameterList)), "ParameterList" },
    { std::type_index(typeid(bool)), "bool" },
    { std::type_index(typeid(char)), "char" },
    { std::type_index(typeid(double)), "double" },
    { std::type_index(typeid(int)), "int" },
    { std::type_index(typeid(std::string)), "string" },
};
