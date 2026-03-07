import { useState } from "react";
import FormInput from "../../components/forms/FormInput";
import { Loading } from "../../components/utils/Loading";

export function MountItem({
    mount,
    index,
    mountInputs,
    onChange,
    onRemove,
    onDeleteFromRepo,
    canRemove
}) {
    const [removing, setRemoving] = useState(false);

    const handleRemove = async () => {
        try {
            setRemoving(true);
            if (mount?.msdbsm_id) {
                await onDeleteFromRepo(mount.msdbsm_id);
            }
            onRemove(index);
        } catch (err) {
            console.error(err);
        } finally {
            setRemoving(false);
        }
    };

    return (
        <div className="border rounded p-3 mb-3">
            <div className="d-flex justify-content-between align-items-center">
                <strong>Mount #{index + 1}</strong>

                {canRemove && (
                    <button
                        type="button"
                        className="btn btn-sm btn-danger"
                        onClick={handleRemove}
                        disabled={removing}
                    >
                        {removing ? "Removing..." : "Remove"}
                    </button>
                )}
            </div>

            {removing ? (
                <div style={{ minHeight: "158px", position:"relative" }}>
                <Loading tags="divs"/>
                </div>
            ) : (
                mountInputs.map((input) => (
                    <FormInput
                        key={input.name}
                        {...input}
                        value={mount[input.name]}
                        onChange={(e) => onChange(index, e)}
                    />
                ))
            )}
        </div>
    );
}
