/*
 * Copyright (c) 2012 Oleksandr Sviridenko
 */

#ifndef __LES_READERS_CELAR_HPP
#define __LES_READERS_CELAR_HPP

#include "../packed_matrix.hpp"

/**
 * Parsing \c var_txt file:
 *
 * \li \b Field 1: the variable number. ATTENTION, the numbers are not
 * necessary in sequence. Some instances actually involve only a subet
 * of the variable of the original problem.
 * \li \b Field 2: the domain number for the variable (cf. dom.txt file).
 * \li \b Field 3: the initial value of the variable (if any). This field is
 * not always present. If present, it means that the link has laready
 * been assigned a frequency.
 * \li \b Field 4: mobility of the variable i.e., the index of the cost of
 * modification of its value (cf. cst.txt). The mobility can be equal
 * to 0, 1 2, 3 et 4. A mobility equal to 0 indicates that the
 * variable value cannot be modified (hard constraint). The values
 * from 1 to 4 corresponds to increasing penalties whose values are
 * defined in the cst.txt file.
 *
 * Parsing \c ctr_txt file:
 *
 * \li \b Field 1: the number of the first variable.
 * \li \b Field 2: the number of the second variable.
 * \li \b Field 3: the constraint type. It is defined by a single character:
 * (D (difference), C (cosite), F (fixe), P (préfixé) ou L (far
 * fields). This field is useless in practice and is only available
 * here to identify the origin of the constraint.
 * \li \b Field 4: the operator used in the constraint (see next
 * field). It can be "=" or ">".
 * \li \b Field 5: the constraint deviation. It defines the constant k12
 * already mentionned. Together, Fields 4 and 5 define the
 * constraint. The Field 4 indicates the realtional operator that must
 * be used to compare the absolute value of the difference of the
 * values of the variables to the integer given in the field 5
 * (deviation). The semnatics of a constraint is therefore:
 *
 *  |Field1 - Field2| Field4 Field5
 *
 * \li \b Field 6: The index of weighting of the constraint. As for the
 * mobility of assigned variables, it is an index that varies from 0
 * to 4. Value 0 indicates a hard constraint. Values from 1 to 4
 * indicates increasing weights as given in the \c cst_txt field. If this
 * field is absent from the file, the constraint must be considered as
 * an hard constraint (index 0).
 */
class CELARReader
{
public:
  CELARReader() { }

  void read(const char* var_txt, const char* dom_txt,
            const char* ctr_txt, const char* cst_txt);

  inline const PackedMatrix& get_cons_matrix() { return _cons_matrix; }

private:
  PackedMatrix _cons_matrix;
};

#endif /* __LES_READERS_CELAR_HPP */
