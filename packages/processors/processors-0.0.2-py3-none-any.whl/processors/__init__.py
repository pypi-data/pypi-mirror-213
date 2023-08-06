# SPDX-FileCopyrightText: 2023-present fenke <fenke@live.com>
#
# SPDX-License-Identifier: MIT
import typing
import inspect
import logging

syslog = logging.getLogger(__name__)


class AnnotatedDataProcessor(): # pylint: disable=too-few-public-methods
    """
        Mixin class to can the data processing function
        The function is expected to have a signature
        matching either

        async func(data:pandas.DataFrame, ...)

        or

        async func(data:numpy.ndarray, ...)


        The additional keyword arguments are expected to be fully annotated,
        defaults allowed. The annotations will be used to retrieve arguments
        from mixin classes.

        provides:
            process

        requires:
            get_parameter(parameter_name, parameter_type, parameter_default, **kwargs)
            get_data(data_type:annotation, **kwargs)
            use_result(resultdata, **kwargs)
    """

    def __init__(self, processor:typing.Awaitable, **kwargs):

        super().__init__(**kwargs)

        self.processor = processor

        # Use introspection to get the function parameters, ignore the return
        self.processor_parameters = dict(inspect.signature(processor).parameters)
        self.return_parameter = self.processor_parameters.pop('return', None)

        # The first parameter is the data, split this off since data
        # is obtained through get_data, not get_param
        data_arg, *callargs = list(self.processor_parameters.keys())
        self.data_type = self.processor_parameters[data_arg].annotation
        self.call_args = {
            N:{
                'parameter_name'    :self.processor_parameters[N].name,
                'parameter_type'    :self.processor_parameters[N].annotation,
                'parameter_default' :self.processor_parameters[N].default
            }
            for N in callargs
        }

    async def process(self, **kwargs):
        # pylint: disable=no-member, C0116, W0718, W1203
        callargs = {
            K: self.get_parameter(**A, **kwargs)
            for K, A in self.call_args.items()
        }
        calldata = await self.get_data(self.data_type, **kwargs)

        try:
            return await self.use_result(
                await self.processor(
                    calldata,
                    **callargs),
                **kwargs)

        except Exception as something_went_wrong:
            syslog.exception(f"Exception: {repr(something_went_wrong)}", exc_info=True)

