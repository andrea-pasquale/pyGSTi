"""
Defines the LayerLizard class and supporting functionality.
"""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************


from pygsti.modelmembers import operations as _op


class LayerRules(object):
    """
    TODO: docstring
    """

    def _create_op_for_circuitlabel(self, model, circuitlbl):
        """
        A helper method for derived classes used for processing :class:`CircuitLabel` labels.

        (:class:`CircuitLabel` labels encapsulate sub-circuits repeated some integer number of times).

        This method build an operator for `circuitlbl` by creating a composed-op
        (using :class:`ComposedOp`) of the sub-circuit that is exponentiated (using
        :class:`RepeatedOp`) to the power `circuitlbl.reps`.

        Parameters
        ----------
        circuitlbl : CircuitLabel
            The (sub-circuit)^power to create an operator for.

        Returns
        -------
        LinearOperator
        """
        if len(circuitlbl.components) != 1:  # works for 0 components too
            subCircuitOp = _op.ComposedOp([model.circuit_layer_operator(l, 'op') for l in circuitlbl.components],
                                          evotype=model.evotype, state_space=model.state_space)
        else:
            subCircuitOp = model.circuit_layer_operator(circuitlbl.components[0], 'op')
        if circuitlbl.reps != 1:
            #finalOp = _op.ComposedOp([subCircuitOp]*circuitlbl.reps,
            #                         evotype=model.evotype, state_space=model.state_space)
            finalOp = _op.RepeatedOp(subCircuitOp, circuitlbl.reps, evotype=model.evotype)
        else:
            finalOp = subCircuitOp

        model._init_virtual_obj(finalOp)  # so ret's gpindices get set, essential for being in cache
        return finalOp

    def prep_layer_operator(self, model, layerlbl, cache):
        """
        Create the operator corresponding to `layerlbl`.

        Parameters
        ----------
        layerlbl : Label
            A circuit layer label.

        Returns
        -------
        State
        """
        #raise KeyError(f"Cannot create operator for non-primitive prep layer: {layerlbl}")
        raise KeyError("Cannot create operator for non-primitive prep layer: %s" % str(layerlbl))

    def povm_layer_operator(self, model, layerlbl, cache):
        """
        Create the operator corresponding to `layerlbl`.

        Parameters
        ----------
        layerlbl : Label
            A circuit layer label.

        Returns
        -------
        POVM or POVMEffect
        """
        #raise KeyError(f"Cannot create operator for non-primitive prep layer: {layerlbl}")
        raise KeyError("Cannot create operator for non-primitive prep layer: %s" % str(layerlbl))

    def operation_layer_operator(self, model, layerlbl, cache):
        """
        Create the operator corresponding to `layerlbl`.

        Parameters
        ----------
        layerlbl : Label
            A circuit layer label.

        Returns
        -------
        LinearOperator
        """
        #raise KeyError(f"Cannot create operator for non-primitive layer: {layerlbl}")
        raise KeyError("Cannot create operator for non-primitive layer: %s" % str(layerlbl))


#REMOVE
# ----------------------------- OLD -------------------------------
#class ExplicitLayerLizard(LayerLizard):
#    """
#    A layer lizard that only serves up layer operations it have been explicitly provided upon initialization.
#
#    Parameters
#    ----------
#    preps : OrderedMemberDict
#        Dictionary of simplified state preparation layer operations
#        available for serving to a forwared simulator.
#
#    operations : OrderedMemberDict
#        Dictionary of simplified layer operations available for
#        serving to a forwared simulator.
#
#    povms : OrderedMemberDict
#        Dictionary of simplified measurement layer operations
#        available for serving to a forwared simulator.
#
#    instruments : OrderedMemberDict
#        Dictionary of simplified instrument layer operations
#        available for serving to a forwared simulator.
#
#    model : Model
#        The model associated with the simplified operations.
#    """
#
#    def __init__(self, preps, operations, povms, instruments, model):
#        """
#        Creates a new ExplicitLayerLizard.
#
#        Parameters
#        ----------
#        preps, operations, povms, instruments : OrderedMemberDict
#            Dictionaries of simplified layer operations available for
#            serving to a forwared simulator.
#
#        model : Model
#            The model associated with the simplified operations.
#        """
#        simplified_effects = _collections.OrderedDict()
#        for povm_lbl, povm in povms.items():
#            for k, e in povm.simplify_effects(povm_lbl).items():
#                simplified_effects[k] = e
#
#        simplified_ops = _collections.OrderedDict()
#        for k, g in operations.items(): simplified_ops[k] = g
#        for inst_lbl, inst in instruments.items():
#            for k, g in inst.simplify_operations(inst_lbl).items():
#                simplified_ops[k] = g
#
#        #Note: maybe copies not needed here?
#        self.preps = {k: v for k, v in preps.items()}  # no compilation needed
#        self.operations = {k: v for k, v in operations.items()}  # shallow copy
#        self.povms = {k: v for k, v in povms.items()}
#        self.instruments = {k: v for k, v in instruments.items()}
#
#        self.simpleops = simplified_ops
#        self.effects = simplified_effects
#        super(ExplicitLayerLizard, self).__init__(model)
#
#    def evotype(self):
#        """
#        Return the evolution type of the operations being served.
#
#        Returns
#        -------
#        str
#        """
#        return self.model._evotype
#
#    def prep(self, layerlbl):
#        """
#        Return the (simplified) preparation layer operator given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The preparation layer label.
#
#        Returns
#        -------
#        LinearOperator
#        """
#        return self.preps[layerlbl]
#
#    def effect(self, layerlbl):
#        """
#        Return the (simplified) POVM effect layer operator given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The effect layer label
#
#        Returns
#        -------
#        LinearOperator
#        """
#        return self.effects[layerlbl]
#
#    def operation(self, layerlbl):
#        """
#        Return the (simplified) layer operation given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The circuit (operation-) layer label.
#
#        Returns
#        -------
#        LinearOperator
#        """
#        if isinstance(layerlbl, _CircuitLabel):
#            dense = bool(self.model._sim_type == "matrix")  # whether dense matrix gates should be created
#            return self._create_op_for_circuitlabel(layerlbl, dense)
#        else:
#            return self.simpleops[layerlbl]
#
#    def from_vector(self, v, close=False, nodirty=False):
#        """
#        Re-initialize the simplified operators from model-parameter-vector `v`.
#
#        Parameters
#        ----------
#        v : numpy.ndarray
#            A vector of parameters for `Model` associated with this layer lizard.
#
#        close : bool, optional
#            Set to `True` if `v` is close to the current parameter vector.
#            This can make some operations more efficient.
#
#        nodirty : bool, optional
#            If True, the framework for marking and detecting when operations
#            have changed and a Model's parameter-vector needs to be updated
#            is disabled.  Disabling this will increases the speed of the call.
#
#        Returns
#        -------
#        None
#        """
#        for _, obj in _itertools.chain(self.preps.items(),
#                                       self.effects.items(),
#                                       self.simpleops.items(),
#                                       self.opcache.items()):
#            obj.from_vector(v[obj.gpindices], close, nodirty)
#
#
#class ImplicitLayerLizard(LayerLizard):
#    """
#    A base class for objects which serve up layer operations for implicit models.
#
#    This layer lizard (see :class:`LayerLizard`) is used as a base class for
#    objects which serve up layer operations for implicit models (and so provide
#    logic for how to construct layer operations from model components).
#
#    Parameters
#    ----------
#    prep_blks : dict
#        Dictionary of :class:`OrderedMemberDict` objects, one per
#        "category" of state preparations.  These are stored and used
#        to build layer operations for serving to a forward simulator.
#
#    op_blks : dict
#        Dictionary of :class:`OrderedMemberDict` objects, one per
#        "category" of operations.  These are stored and used
#        to build layer operations for serving to a forward simulator.
#
#    povm_blks : dict
#        Dictionary of :class:`OrderedMemberDict` objects, one per
#        "category" of POVMs.  These are stored and used
#        to build layer operations for serving to a forward simulator.
#
#    instrument_blks : dict
#        Dictionary of :class:`OrderedMemberDict` objects, one per
#        "category" of instruments.  These are stored and used
#        to build layer operations for serving to a forward simulator.
#
#    model : Model
#        The model associated with the operations.
#    """
#
#    def __init__(self, prep_blks, op_blks, povm_blks, instrument_blks, model):
#        """
#        Creates a new ImplicitLayerLizard.
#
#        Parameters
#        ----------
#        prep_blks, op_blks, povm_blks, instrument_blks : dict
#            Dictionaries of :class:`OrderedMemberDict` objects, one per
#            "category" of operators.  These are stored and used
#            to build layer operations for serving to a forwared simulator.
#
#        model : Model
#            The model associated with the operations.
#        """
#        #Create dicts of all "POVMName_EffectName" effects, one dict per category
#        # This simplification also ensures all gpindices are pointing to the parent model's paramvec
#        simplified_effect_blks = _collections.OrderedDict()
#        for povm_dict_lbl, povmdict in povm_blks.items():
#            simplified_effect_blks[povm_dict_lbl] = _collections.OrderedDict(
#                [(k, e) for povm_lbl, povm in povmdict.items()
#                 for k, e in povm.simplify_effects(povm_lbl).items()])
#
#        simplified_op_blks = op_blks.copy()  # no compilation needed
#        for inst_dict_lbl, instdict in instrument_blks.items():
#            if inst_dict_lbl not in simplified_op_blks:  # only create when needed
#                simplified_op_blks[inst_dict_lbl] = _collections.OrderedDict()
#            for inst_lbl, inst in instdict.items():
#                for k, g in inst.simplify_operations(inst_lbl).items():
#                    simplified_op_blks[inst_dict_lbl][k] = g
#
#        self.prep_blks = prep_blks.copy()  # no compilation needed
#        self.operation_blks = op_blks.copy()  # shallow copy of normal dict
#        self.povm_blks = povm_blks.copy()
#        self.instrument_blks = instrument_blks.copy()
#
#        self.simpleop_blks = simplified_op_blks
#        self.effect_blks = simplified_effect_blks
#        super(ImplicitLayerLizard, self).__init__(model)
#
#    def prep(self, layerlbl):
#        """
#        Return the (simplified) preparation layer operator given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The preparation layer label.
#
#        Returns
#        -------
#        LinearOperator
#        """
#        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `get_preps`")
#
#    def effect(self, layerlbl):
#        """
#        Return the (simplified) POVM effect layer operator given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The effect layer label
#
#        Returns
#        -------
#        LinearOperator
#        """
#        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `effect`")
#
#    def operation(self, layerlbl):
#        """
#        Return the (simplified) layer operation given by `layerlbl`.
#
#        Parameters
#        ----------
#        layerlbl : Label
#            The circuit (operation-) layer label.
#
#        Returns
#        -------
#        LinearOperator
#        """
#        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `operation`")
#
#    def evotype(self):
#        """
#        Return the evolution type of the operations being served.
#
#        Returns
#        -------
#        str
#        """
#        return self.model._evotype
#
#    def from_vector(self, v, close=False, nodirty=False):
#        """
#        Re-initialize the simplified operators from model-parameter-vector `v`.
#
#        Parameters
#        ----------
#        v : numpy.ndarray
#            A vector of parameters for `Model` associated with this layer lizard.
#
#        close : bool, optional
#            Set to `True` if `v` is close to the current parameter vector.
#            This can make some operations more efficient.
#
#        nodirty : bool, optional
#            If True, the framework for marking and detecting when operations
#            have changed and a Model's parameter-vector needs to be updated
#            is disabled.  Disabling this will increases the speed of the call.
#
#        Returns
#        -------
#        None
#        """
#        for _, objdict in _itertools.chain(self.prep_blks.items(),
#                                           self.effect_blks.items(),
#                                           self.simpleop_blks.items()):
#            for _, obj in objdict.items():
#                obj.from_vector(v[obj.gpindices], close, nodirty)
#
#        for _, obj in self.opcache.items():
#            obj.from_vector(v[obj.gpindices], close, nodirty)