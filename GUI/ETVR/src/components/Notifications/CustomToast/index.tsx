import { Transition, Toast } from 'solid-headless'
import { createSignal, Component } from 'solid-js'
import CloseIcon from '@src/components/CloseIcon'
import { notifications } from '@src/store/ui/selectors'

interface ToastProps {
    id: string
    message: string
}

const CustomToast: Component<ToastProps> = (props) => {
    const [isOpen, setIsOpen] = createSignal(true)

    const dismiss = () => {
        setIsOpen(false)
    }

    return (
        <Transition
            show={isOpen()}
            class="relative transition rounded-lg p-4 bg-slate-600"
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-50"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-50"
            afterLeave={() => {
                notifications()?.remove(props.id)
            }}>
            <Toast class="flex justify-between items-center">
                <span class="flex-1 text-sm font-semibold text-gray-50">{props.message}</span>
                <button
                    type="button"
                    class="bg-rose-600 hover:bg-rose-700 focus:bg-rose-900 flex-none w-6 h-6 p-1 ml-1 text-gray-50 rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
                    onClick={dismiss}>
                    <CloseIcon />
                </button>
            </Toast>
        </Transition>
    )
}

export default CustomToast
